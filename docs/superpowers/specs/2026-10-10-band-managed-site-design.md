# Band-Managed Site: Pages CMS + Hugo — Design

**Date:** 2026-10-10
**Author:** Ian Chesal (with Claude)
**Status:** Draft for review

## Goal

Make crawlspacenh.com something the remaining band members (Bobby, Mike, Andy, and
future members) can update from a phone without knowing Git, Markdown, or how a deploy
works — at zero cost and with near-zero ongoing maintenance, because Ian is leaving the
band and nobody will be maintaining application code.

### Success criteria

- A band member can add a gig, add a venue, upload a poster, and edit the band roster
  through a form-based admin, and see it live within a few minutes.
- Past gigs leave the Live page automatically and appear on a Past Shows page, with no
  manual cleanup.
- The site has no runtime: no servers, databases, or app code to patch. If the admin tool
  ever disappears, editing falls back to the GitHub web editor with nothing lost.
- Hosting stays free.
- No part of the site depends on Ian's personal accounts, except DNS (see Out of scope).

### Decisions already made

- **Rejected: custom Hono app on Cloudflare Workers + D1/R2.** It fits the free tier but
  would hand Bobby (technical, but not a developer) an application to maintain: auth,
  uploads, migrations, dependency drift. Too much liability for a band site.
- **Rejected: hosted site builders** (Squarespace, Wix, etc.). Not free.
- **Chosen: keep Hugo on GitHub Pages and add [Pages CMS](https://pagescms.org)** as a
  hosted, Git-backed form editor. Content stays as plain files in the repo. Pages CMS
  needs one config file (`.pages.yml`) and can be removed without affecting the site.
- **Look and feel, option A:** band members edit content (images, tagline, text) but not
  colors or fonts. A one-time redesign sets those in code. The redesign is a separate
  spec.

## Architecture

```
 Band member ──▶ app.pagescms.org ──commit──▶ GitHub: crawlspacenh/crawlspacenh.github.io
 (GitHub login                                           │
  or email invite)                                       ▼
                              GitHub Actions: hugo --minify  (on push to main + nightly)
                                                         │
                                                         ▼
 Visitor ──▶ crawlspacenh.com ──DNS (Ian's Cloudflare)──▶ GitHub Pages
                                    contact form ──▶ Formspree (crawlspacenhband@gmail.com)
```

- **Unchanged:** Hugo, GitHub Pages, the `CNAME` file, the deploy workflow
  (`.github/workflows/hugo.yaml`), the Formspree endpoint, Google Analytics.
- **Added:** `.pages.yml`; Hugo layouts that render gigs, venues, band, videos, and site
  settings from data; a nightly scheduled rebuild; a CI build check on `main`.
- **Removed:** the `themes/hugo-split-theme` git submodule (it points at Ian's personal
  repo `ianchesal/hugo-split-theme`; vendor it into the repo as plain files);
  `update-posters.sh` and `scripts/update-posters.py` (the Posters page becomes a
  template); per-page inline `<style>` blocks (moved into one shared stylesheet).

## Content model

### Gigs — `content/gigs/YYYY-MM-DD-<venue-slug>.md`

One file per show, front matter only (TOML, per repo convention). Pages CMS builds the
filename from date and venue.

| Field        | Type                | Required | Notes                                                    |
|--------------|---------------------|----------|----------------------------------------------------------|
| `date`       | date                | yes      | Show date                                                |
| `start`      | string              | yes      | Free text, e.g. "6:30 pm". Admin default: "6:00 pm"      |
| `end`        | string              | no       | Free text                                                |
| `venue`      | reference → Venues  | yes      | Venue slug, chosen from a dropdown                       |
| `title`      | string              | no       | Named events, e.g. "Rock and Roll Playhouse"             |
| `poster`     | image               | no       | Stored under `assets/images/posters/`                    |
| `ticket_url` | string              | no       | Rendered only when present                               |
| `notes`      | text                | no       | Short line, e.g. "All ages"                              |
| `cancelled`  | boolean             | no       | Default false; gig stays listed with a "Cancelled" badge |

Gig pages are not rendered individually (`build.render = "never"` via cascade); gigs exist
only as data for list templates.

### Venues — `data/venues/<slug>.yml`

One file per venue so each is a separate admin entry. Fields: `name`, `url`, `street`,
`city`, `state`, `zip`, `map_url`. The filename slug is the key gigs reference.

### Band — `data/band.yml`

Ordered list; list order is display order. Each member: `name`, `instruments` (list of
strings), `photo` (image under `assets/images/band/`).

### Videos — `data/videos.yml`

List of `title`, `youtube_url`. Rendered as privacy-enhanced YouTube embeds.

### Site settings — `data/site.yml`

`tagline`, `hero_image`, `background_image`, `booking_email`, `social_links` (list of
`label`, `url`, `new_tab`). No colors or fonts (option A). The navigation links currently
in `hugo.toml` `params.links` move here so the band can edit them.

### Free-form pages

`content/about.md`, `content/merch.md`, `content/contact.md`: rich-text body. The
Formspree contact form moves from `contact.md` into a layout/partial so it cannot be
broken by a content edit; the page body is the intro text above the form.

## Page rendering

| URL            | Source                         | Behavior                                                          |
|----------------|--------------------------------|-------------------------------------------------------------------|
| `/`            | `site.yml` + gigs              | Hero, tagline, "Next shows" (next 3 upcoming gigs)                |
| `/live`        | gigs                           | Upcoming gigs, ascending by date                                  |
| `/live/past`   | gigs                           | Past gigs, descending, grouped by year                            |
| `/posters`     | gigs + `assets/images/posters` | Every gig poster, newest first, plus orphan poster images         |
| `/the-band`    | `band.yml`                     | Roster in list order                                              |
| `/videos`      | `videos.yml`                   | Embeds                                                            |
| `/about`, `/merch`, `/contact` | Markdown pages | As today                                                    |

Existing `uglyURLs = true` output (`live.html`, etc.) is preserved so current inbound
links keep working; `/live/past` renders as `live/past.html`.

### Upcoming vs. past

- A gig is **upcoming** when `date >= today` in `America/New_York` (set Hugo `timeZone`),
  so a show stays listed through its own evening.
- The split happens at build time. A nightly scheduled build (`schedule: cron` at 08:00
  UTC, about 4am ET) rolls gigs over the morning after.
- **Backstop:** a small inline script on `/live` and the home "Next shows" hides any
  entry whose `data-date` is before the visitor's today, so a missed nightly build never
  shows a stale gig.
- Gigs carry schema.org `MusicEvent` structured data (per repo guidelines), including
  `eventStatus: EventCancelled` when `cancelled` is true.

### Posters page

All gigs with a `poster`, newest first, captioned with date and venue. Then any image in
`assets/images/posters/` not referenced by a gig, ordered by filename descending
(filenames are dates). This covers 2023–2024 posters with no matching gig data.

## Images

- All CMS-managed images live in `assets/images/{posters,band,site}/` so Hugo's image
  pipeline can process them. Templates generate responsive WebP variants (with a JPEG
  fallback) at a few widths, so uploading full-size phone photos is fine.
- Originals stay in the repo. Current total is about 52 MB, growing about 15–20 posters
  a year, far below GitHub's soft limits.
- **To verify during planning:** that Pages CMS media `input`/`output` config supports
  storing in `assets/` with the path format templates expect. **Fallback:** keep images
  in `static/images/` and skip resizing.
- Every rendered image has alt text: for posters, "Poster for <venue>, <date>"; for band
  photos, the member's name.

## Admin (Pages CMS) — `.pages.yml`

- **Sidebar:** Gigs, Venues, Band, Videos, Pages (About, Merch, Contact), Site settings,
  Media.
- **Gigs view:** columns date / venue / title, sorted by date descending.
- **Access:** Bobby signs in with his GitHub account (`feldspar88-web`). Other members
  are invited by email as Pages CMS collaborators and need no GitHub account.
- **Attribution:** `settings.commit.identity: user` so commits carry the editor's name.
- **Undo:** every save is a Git commit and can be reverted in GitHub.

## Build, deploy, and guardrails

- `.github/workflows/hugo.yaml`: add `schedule:` (nightly) next to the existing `push`
  and `workflow_dispatch` triggers. Deploy only runs if the Hugo build succeeds, so a bad
  edit leaves the last good site live.
- Templates fail the build (`errorf`) when a gig references a venue that doesn't exist,
  rather than rendering a broken entry.
- `.github/workflows/pr-tests.yml` (Hugo build + htmltest) stays the PR check.

## Migration

All work happens on a feature branch. The current branch name `convert-to-cloudflare` is
now misleading; Ian decides whether to rename it.

1. Vendor `hugo-split-theme` into the repo (copy the files in, remove the submodule and
   `.gitmodules` entry).
2. Build layouts for gigs, past shows, posters, band, videos, home "next shows", and the
   contact form partial. Consolidate inline page styles into one stylesheet with **no
   visual change**; the redesign is separate.
3. One-time migration script in `scripts/migrate/` (deleted after cutover):
   - Parse every historical revision of `content/live.md` (45 distinct gig dates
     recoverable as of 2026-10-10) into gig files plus a deduplicated venue list.
   - Match posters to gigs by date; move posters to `assets/images/posters/`.
   - Convert `the-band.md` to `data/band.yml` (current lineup: Mike D'Amante, Andy
     Boeckeler, Bobby Decorte; John Jordan and Ian Chesal removed) and fix the page meta
     description, which still names John and Ian.
   - Move `hugo.toml` `params.links` and social/site params into `data/site.yml`.
4. Ian reviews the seeded data and fixes venue duplicates and typos by hand.
5. Add `.pages.yml`, the nightly schedule, and build-time venue validation.
6. Update `CLAUDE.md` and `README.md` for the new structure; write
   `docs/editing-the-site.md`, a plain-language guide for band members (add a gig, add a
   venue, upload a poster, edit the band, undo a mistake).

## Cutover

1. Open a PR; review the CI build. Merging to `main` deploys.
2. Connect the repo at app.pagescms.org; invite Mike and Andy by email.
3. 15-minute walkthrough with Bobby: add a gig, add a venue, upload a poster, fix a typo,
   revert a change.
4. Make Bobby and a GitHub account on `crawlspacenhband@gmail.com` owners of the
   `crawlspacenh` org. Ian removes himself when ready.

## Testing

- Per this repo's `CLAUDE.md`, Claude doesn't run the site to test changes; Ian tests
  manually.
- Automated: the Hugo build in CI (catches template errors and missing venues) and the
  existing htmltest link check.
- Manual checklist for Ian:
  - Gigs dated yesterday, today, and tomorrow land on the right page.
  - A cancelled gig shows the badge and correct structured data.
  - A gig with no poster renders cleanly.
  - Editing a venue updates every gig that uses it.
  - A full-size phone photo uploaded as a poster renders resized.
  - The contact form still submits to Formspree.
  - Old URLs (`live.html`, `posters.html`, etc.) still resolve.

## Out of scope

- **Visual redesign:** separate spec, written after this lands.
- **DNS:** the `crawlspacenh.com` zone stays in Ian's personal Cloudflare account for now.
  Known dependency on Ian; moving it to a band-owned account is a later follow-up.
- **Gig history before 2025:** only what poster filenames provide.
- **Mailing lists, ticketing, calendar feeds.**
