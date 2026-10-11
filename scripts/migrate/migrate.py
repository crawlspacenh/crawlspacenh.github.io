#!/usr/bin/env python3
"""One-time migration of gig history into Pages CMS data files.

Run from the repo root:  python3 scripts/migrate/migrate.py
Writes content/gigs/*.md, data/venues/*.yml and scripts/migrate/REPORT.md.
Delete scripts/migrate/ after cutover.
"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gigdata import (  # noqa: E402
    build_venues,
    gig_filename,
    gig_front_matter,
    parse_blocks,
    select_gigs,
    venue_yaml,
)

ROOT = Path(__file__).resolve().parents[2]
LIVE = "content/live.md"
POSTERS = ROOT / "assets/images/posters"
GIGS_DIR = ROOT / "content/gigs"
VENUES_DIR = ROOT / "data/venues"
REPORT = Path(__file__).resolve().parent / "REPORT.md"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def load_revisions():
    revisions = []
    for line in git("log", "--reverse", "--format=%H %cI", "--", LIVE).splitlines():
        sha, iso = line.split(" ", 1)
        revisions.append((datetime.fromisoformat(iso).date(), parse_blocks(git("show", f"{sha}:{LIVE}"))))
    return revisions


def find_poster(day) -> str | None:
    matches = sorted(POSTERS.glob(f"{day.isoformat()}.*"))
    return f"/images/posters/{matches[0].name}" if matches else None


def main() -> None:
    kept, dropped = select_gigs(load_revisions())
    kept.sort(key=lambda g: (g.date, g.start))
    venues, gig_venue, names = build_venues(kept)

    GIGS_DIR.mkdir(parents=True, exist_ok=True)
    VENUES_DIR.mkdir(parents=True, exist_ok=True)
    for slug, venue in venues.items():
        (VENUES_DIR / f"{slug}.yml").write_text(venue_yaml(venue), encoding="utf-8")

    written: list[tuple[str, object]] = []
    used_posters: set[str] = set()
    taken: set[str] = set()
    for i, gig in enumerate(kept):
        name = gig_filename(gig, gig_venue[i])
        stem, n = name.removesuffix(".md"), 2
        while name in taken:
            name, n = f"{stem}-{n}.md", n + 1
        taken.add(name)
        poster = find_poster(gig.date)
        if poster in used_posters:
            poster = None
        if poster:
            used_posters.add(poster)
        (GIGS_DIR / name).write_text(gig_front_matter(gig, gig_venue[i], poster), encoding="utf-8")
        written.append((name, gig))

    orphans = sorted(p.name for p in POSTERS.iterdir() if f"/images/posters/{p.name}" not in used_posters)
    lines = [
        "# Migration report",
        "",
        f"{len(written)} gigs and {len(venues)} venues written. Review everything below, then fix by hand.",
        "",
        "## Dropped gigs (removed before their date, probably cancelled)",
        "",
        *[f"- {g.date} at {g.venue_name or '(no venue)'}" for g in dropped],
        "",
        "## Venues",
        "",
        "Merge duplicates (same place, different link) by editing gig `venue` values and deleting the extra file.",
        "",
    ]
    for slug, venue in sorted(venues.items()):
        missing = [k for k in ("street", "city", "zip", "map_url") if not venue[k]]
        seen = sorted(names[slug])
        lines.append(f"- `{slug}`: {venue['name']}"
                     + (f"; names seen: {', '.join(seen)}" if len(seen) > 1 else "")
                     + (f"; missing: {', '.join(missing)}" if missing else ""))
    lines += [
        "",
        "## Gigs with notes",
        "",
        "Notes often hold an event title or room name that belongs in `title` or the venue.",
        "",
        *[f"- `{name}`: {'; '.join(g.notes)}" for name, g in written if g.notes],
        "",
        "## Posters with no gig",
        "",
        *[f"- {name}" for name in orphans],
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(written)} gigs, {len(venues)} venues, {len(dropped)} dropped. See {REPORT}")


if __name__ == "__main__":
    main()
