"""Pure helpers for the one-time content/live.md -> gig data migration.

Delete scripts/migrate/ after cutover.
"""
from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from urllib.parse import urlparse

HEADING = re.compile(r"^#\s+[A-Za-z]+day,\s+([A-Za-z]+ \d{1,2}, \d{4})$")
TIME = re.compile(
    r"^(?P<start>\d{1,2}(?::\d{2})?\s*[ap]m)\s*-\s*(?P<end>\d{1,2}(?::\d{2})?\s*[ap]m)"
    r"\s*ET\b\s*(?P<rest>.*)$",
    re.IGNORECASE,
)
LINK = re.compile(r"^\[(?P<text>[^\]]+)\]\((?P<url>[^)]+)\)$")
MAP = re.compile(r"\(\s*\[map\]\((?P<url>[^)]+)\)\s*\)")
CITY = re.compile(r"^(?P<city>[A-Za-z .'-]+),\s*(?P<state>[A-Z]{2})(?:\s+(?P<zip>\d{5}))?$")
VENUE_FIELDS = ("name", "url", "street", "city", "state", "zip", "map_url")


@dataclass
class Gig:
    date: date
    start: str = ""
    end: str = ""
    venue_name: str = ""
    venue_url: str = ""
    street: str = ""
    city: str = ""
    state: str = ""
    zip: str = ""
    map_url: str = ""
    notes: list[str] = field(default_factory=list)


def parse_blocks(text: str) -> list[Gig]:
    """Parse every '# <Weekday>, <Month> <D>, <YYYY>' block in one live.md revision."""
    gigs: list[Gig] = []
    current: Gig | None = None
    for raw in text.splitlines():
        heading = HEADING.match(raw.strip())
        if heading:
            try:
                day = datetime.strptime(heading.group(1), "%B %d, %Y").date()
            except ValueError:  # typo in history (e.g. "Juuly"): skip the block
                current = None
                continue
            current = Gig(date=day)
            gigs.append(current)
            continue
        if current is None:
            continue
        line = _clean_line(raw)
        if line and not line.startswith("<"):
            _apply_line(current, line)
    return gigs


def _clean_line(raw: str) -> str:
    line = re.sub(r"<br\s*/?>", "", raw.strip(), flags=re.IGNORECASE)
    return html.unescape(line.rstrip("\\").strip())


def _apply_line(gig: Gig, line: str) -> None:
    time = TIME.match(line)
    if time and not gig.start:
        gig.start = _norm_time(time.group("start"))
        gig.end = _norm_time(time.group("end"))
        rest = time.group("rest").strip().strip("()").strip()
        if rest:
            gig.notes.append(rest)
        return
    map_link = MAP.search(line)
    if map_link:
        gig.map_url = map_link.group("url").strip()
        line = MAP.sub("", line).strip()
        if not line:
            return
    link = LINK.match(line)
    if link and not gig.venue_name:
        gig.venue_name = link.group("text").strip()
        gig.venue_url = link.group("url").strip()
        return
    city = CITY.match(line)
    if city and not gig.city:
        gig.city = city.group("city").strip()
        gig.state = city.group("state")
        gig.zip = city.group("zip") or ""
        return
    if not gig.street and line[0].isdigit():
        gig.street = line
        return
    gig.notes.append(line)


def _norm_time(value: str) -> str:
    return re.sub(r"\s*([ap]m)$", r" \1", value.strip().lower())


def select_gigs(revisions: list[tuple[date, list[Gig]]]) -> tuple[list[Gig], list[Gig]]:
    """Pick the gigs that were still listed on the day they happened.

    revisions: (commit date, parsed gigs) in chronological order.
    A gig is kept when it appears in the newest revision committed on or before
    its date, and its fields come from that revision. Otherwise it was removed
    before it happened (probably cancelled) and is returned in `dropped`.
    """
    all_dates = sorted({g.date for _, gigs in revisions for g in gigs})
    kept: list[Gig] = []
    dropped: list[Gig] = []
    for day in all_dates:
        snapshot: list[Gig] = []
        for rev_date, gigs in revisions:
            if rev_date > day:
                break
            snapshot = gigs
        on_day = [g for g in snapshot if g.date == day]
        if on_day:
            kept.extend(on_day)
        else:
            dropped.append([g for _, gigs in revisions for g in gigs if g.date == day][-1])
    return kept, dropped


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ").replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def venue_key(gig: Gig) -> str:
    if gig.venue_url:
        parsed = urlparse(gig.venue_url.lower())
        return parsed.netloc.removeprefix("www.") + parsed.path.rstrip("/")
    return slugify(gig.venue_name)


def build_venues(gigs: list[Gig]) -> tuple[dict[str, dict], dict[int, str], dict[str, set[str]]]:
    """Group gigs into venues by link (or name when there is no link).

    Returns (venue fields by slug, venue slug by gig index, venue names seen by slug).
    Each field comes from the newest gig that has a non-empty value for it.
    """
    groups: dict[str, list[int]] = {}
    for i, gig in enumerate(gigs):
        groups.setdefault(venue_key(gig), []).append(i)
    venues: dict[str, dict] = {}
    gig_venue: dict[int, str] = {}
    names: dict[str, set[str]] = {}
    for idxs in groups.values():
        newest_first = sorted(idxs, key=lambda i: gigs[i].date, reverse=True)
        fields = {}
        for name in VENUE_FIELDS:
            attr = {"name": "venue_name", "url": "venue_url"}.get(name, name)
            fields[name] = next((getattr(gigs[i], attr) for i in newest_first if getattr(gigs[i], attr)), "")
        base = slugify(fields["name"]) or "unknown-venue"
        slug, n = base, 2
        while slug in venues:
            slug, n = f"{base}-{n}", n + 1
        venues[slug] = fields
        names[slug] = {gigs[i].venue_name for i in idxs}
        for i in idxs:
            gig_venue[i] = slug
    return venues, gig_venue, names


def _quote(value: str) -> str:
    # JSON strings are valid TOML basic strings and YAML double-quoted scalars.
    return json.dumps(value, ensure_ascii=False)


def gig_filename(gig: Gig, venue_slug: str) -> str:
    """Matches the Pages CMS template "{fields.date}-{fields.venue}-{fields.start}.md"."""
    return f"{gig.date.isoformat()}-{venue_slug}-{slugify(gig.start) or 'tbd'}.md"


def gig_front_matter(gig: Gig, venue_slug: str, poster: str | None) -> str:
    lines = ["+++", f"date = {gig.date.isoformat()}", f"start = {_quote(gig.start)}"]
    if gig.end:
        lines.append(f"end = {_quote(gig.end)}")
    lines.append(f"venue = {_quote(venue_slug)}")
    if poster:
        lines.append(f"poster = {_quote(poster)}")
    if gig.notes:
        lines.append(f"notes = {_quote('; '.join(gig.notes))}")
    lines += ["cancelled = false", "+++", ""]
    return "\n".join(lines)


def venue_yaml(venue: dict) -> str:
    return "".join(f"{key}: {_quote(str(value))}\n" for key, value in venue.items())
