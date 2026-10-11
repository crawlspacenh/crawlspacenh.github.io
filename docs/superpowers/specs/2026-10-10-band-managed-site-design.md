# Band-Managed Site: Pages CMS + Hugo — Design

**Date:** 2026-10-10
**Author:** Ian Chesal (with Claude)
**Status:** Revised after spec review

## Goal

Make crawlspacenh.com something the remaining band members (Bobby, Mike, Andy, and
future members) can update from a phone without knowing Git, Markdown, or how a deploy
works. It has to be free, and it has to need almost no ongoing maintenance, because Ian
is leaving the band and nobody will be maintaining application code.

### Success criteria

- A band member can add a gig, add a venue, upload a poster, and edit the band roster
  through a form-based admin, and see the change live within a few minutes.
- Past gigs leave the Live page automatically and appear on a Past Shows page, with no
  manual cleanup.
- The site has no runtime: no servers, databases, or app code to patch. If the admin tool
  goes away, editing falls back to the GitHub web editor and nothing is lost.
- When a save breaks the build, a band member is told and the guide says how to recover.
- Hosting stays free.
- The only dependencies on Ian's personal accounts are the ones listed in
  [Accounts and owners](#accounts-and-owners).

### Decisions already made

- **Rejected: a custom Hono app on Cloudflare Workers + D1/R2.** It fits the free tier,
  but it would hand Bobby (technical, not a developer) an application to maintain: auth,
  uploads, migrations, dependency drift.
- **Rejected: hosted site builders** (Squarespace, Wix, etc.). Not free.
- **Chosen: keep Hugo on GitHub Pages and add [Pages CMS](https://pagescms.org)**, a
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
                       .github/workflows/hugo.yaml: hugo --minify
                       (on push to main, nightly schedule, manual)
                          │ success                     │ failure
                          ▼                             ▼
                     GitHub Pages            GitHub issue "Site build failed"
                          ▲                  (emails Bobby + band account)
 Visitor ──▶ crawlspacenh.com (DNS: Ian's Cloudflare)
             contact form ──▶ Formspree (crawlspacenhband@gmail.com)
```

- **Unchanged:** Hugo, GitHub Pages, the `CNAME` file, the Formspree endpoint, Google
  Analytics, `pr-tests.yml` as the PR check.
- **Added:** `.pages.yml`; Hugo layouts that render gigs, venues, band, videos, and site
  settings from data; a nightly schedule and a failure-notification step on the deploy
  workflow.
- **Removed:** the theme git submodule; `update-posters.sh` and
  `scripts/update-posters.py` (the Posters page becomes a template); inline `<style>`
  blocks on pages that become templates; `content/commonmark.md` (theme demo page).

There is no separate CI check on `main`. Pages CMS commits straight to `main`, so the
deploy workflow's Hugo build is the only check band edits go through.

## Content model

### Gigs: `content/gigs/<date>-<venue>-<start>.md`

One file per show, front matter only, in TOML (Pages CMS `format: toml-frontmatter`).
Filename template: `{fields.date}-{fields.venue}-{fields.start}.md`. Including the start
time keeps early and late sets at the same venue on the same date from colliding.

| Field        | Type                | Required | Notes                                                    |
|--------------|---------------------|----------|----------------------------------------------------------|
| `date`       | date                | yes      | Show date                                                |
| `start`      | string              | yes      | Free text, e.g. "6:30 pm". Admin default: "6:00 pm"      |
| `end`        | string              | no       | Free text                                                |
| `venue`      | reference → Venues  | yes      | Stores the venue slug (`value: "{name}"`)                |
| `title`      | string              | no       | Named events, e.g. "Rock and Roll Playhouse"             |
| `poster`     | image               | no       | Stored under `assets/images/posters/`                    |
| `ticket_url` | string              | no       | Rendered only when present                               |
| `notes`      | text                | no       | Short line, e.g. "All ages"                              |
| `cancelled`  | boolean             | no       | Default false; gig stays listed with a "Cancelled" badge |

- Gigs use Hugo's `date` field, so `hugo.toml` sets **`buildFuture = true`**. Without it,
  Hugo leaves out every future-dated page and `/live` is always empty. No other content
  has a future `date`.
- `content/gigs/_index.md` sets a cascade of `build = { render = "never", list = "always" }`
  for gig pages, and `build = { render = "never" }` for the section itself. Neither
  individual gig pages nor a `/gigs.html` list page is produced; gigs exist only as data.

### Venues: `data/venues/<slug>.yml`

One file per venue, so each is a separate admin entry. Fields: `name`, `url`, `street`,
`city`, `state`, `zip`, `map_url`. The filename slug is the key that gigs reference.

**Missing venue:** if a gig names a venue file that doesn't exist (for example, someone
deleted or renamed it), the template prints the slug as plain text with no address, and
the build logs a warning (`warnf`). The build doesn't fail, so one bad reference can't
block every later edit.

### Band: `data/band.yml`

An ordered list; list order is display order. Each member has `name`, `instruments` (a
list of strings), and `photo` (an image under `assets/images/band/`).

### Videos: `data/videos.yml`

A list of entries, each with `title`, `date`, `description`, and `youtube_url`. The
template accepts both video URLs (`?v=<id>` or `youtu.be/<id>`) and playlist URLs
(`?list=<id>`), and embeds them as `embed/<id>` or `embed/videoseries?list=<id>`. The
existing setting `[privacy.youTube] privacyEnhanced = false` stays as it is.

### Site settings: `data/site.yml`

| Field              | Replaces                                      | Template change                                                  |
|--------------------|-----------------------------------------------|------------------------------------------------------------------|
| `tagline`          | `tagline` in `content/_index.md` front matter | `intro.html` reads `site.Data.site.tagline`                      |
| `background_image` | `params.visual.image.file`                    | `split.scss` template reads it and uses the processed image's permalink |
| `share_image`      | `params.shareImage` (file is missing today)   | `head.html` reads it; omit the tag if unset                      |
| `link_groups`      | `params.links`                                | `links.html` reads `site.Data.site.link_groups`                  |

`link_groups` keeps the theme's headed-list structure: a list of `{heading, links: [{text,
url, new_tab}]}`. The current "About" and "Social" groups migrate as they are, including
Bookings, Email, and Facebook. Internal URLs become root-relative (`/the-band.html`).

Email addresses (`booking@`, `tech@`, `fans@`) stay where they are now: in `link_groups`
and in page body text. There are no separate email fields. No colors or fonts (option A).

### Free-form pages

`content/about.md`, `content/merch.md`, and `content/contact.md` have a rich-text body.
The Formspree contact form moves from `contact.md` into a layout partial so a content
edit can't break it; the page body is the intro text above the form.

## Page rendering

| URL                 | Source                         | Behavior                                                        |
|---------------------|--------------------------------|-----------------------------------------------------------------|
| `/`                 | `site.yml` + gigs              | Tagline, plus "Next shows" (see below)                          |
| `/live.html`        | gigs                           | Upcoming gigs, ascending by date; link to Past Shows            |
| `/past-shows.html`  | gigs                           | Past gigs, descending, grouped by year                          |
| `/posters.html`     | gigs + `assets/images/posters` | Every poster, newest first                                      |
| `/the-band.html`    | `band.yml`                     | Roster in list order                                            |
| `/videos.html`      | `videos.yml`                   | Embeds with title, date, description                            |
| `/about.html`, `/merch.html`, `/contact.html` | Markdown pages | As today                                         |

- `uglyURLs = true` and the existing page URLs stay unchanged. Past Shows is a top-level
  page (`content/past-shows.md` with its own `layout`), not nested under `/live/`. This
  keeps every page at the same directory depth, so relative links keep working.
- `head.html` is overridden to output the page's `.Description` and fall back to
  `.Site.Params.description`. Today it only outputs the site-wide value.

### Upcoming vs. past

- `hugo.toml` sets `timeZone = "America/New_York"`; the workflows already set
  `TZ=America/New_York`.
- A gig is **upcoming** when `.Date.Format "2006-01-02"` ≥ `now.Format "2006-01-02"`, a
  string comparison of calendar dates. A gig stays upcoming through the whole day of the
  show, not just until its time of day.
- The split happens at build time. The nightly build (`schedule: cron "0 8 * * *"`,
  about 4am ET) moves gigs to Past Shows the morning after. GitHub can start scheduled
  runs late, sometimes by an hour or more, which doesn't matter here.
- **Backstop:** every rendered gig carries `data-date="YYYY-MM-DD"`. A small inline script
  on `/live.html` and the home page hides any gig dated before the visitor's local date.
  This covers missed or late nightly builds.
- **Home "Next shows":** renders *all* upcoming gigs, and the script shows the first 3
  that aren't hidden. A missed build therefore still shows 3. If JS is off, CSS shows the
  first 3 rendered.
- **Empty states:**
  - `/live.html` with no upcoming gigs: "No shows booked right now. Check back soon, or
    see past shows." The script shows the same message if it ends up hiding every entry.
  - Home with no upcoming gigs: the "Next shows" block isn't shown.
- Gigs carry schema.org `MusicEvent` structured data, with
  `eventStatus: EventCancelled` when `cancelled` is true.

### Posters page

Every image in `assets/images/posters/`, newest first. If a gig uses the poster, it's
captioned with the date and venue. Otherwise it's sorted and captioned by its filename,
since filenames are dates. Each thumbnail links to the full-size original.

## Images

- CMS-managed images live in `assets/images/{posters,band,site}/`. Pages CMS media config:
  `input: assets/images/...`, `output: /images/...`.
- Templates generate WebP at a few widths for display, so full-size phone photos are
  fine to upload. No JPEG fallback.
- **Old image URLs are kept.** The Posters page links each thumbnail to the original
  through the resource's `.RelPermalink`. Hugo publishes the original at the same path it
  has under `assets/`, so `assets/images/posters/2025-01-10.jpg` is served at
  `/images/posters/2025-01-10.jpg`, the URL it has today. Posters shared on social media
  keep working.
- Headshots: `mike-*`, `andy-*`, and `bobby-*` move to `assets/images/band/`.
  `ian-001.jpg` and `john-001.jpg` are deleted (git history keeps them). Old headshot URLs
  aren't preserved.
- `background.jpg` moves to `assets/images/site/`. `crow-*.jpg` stay in `static/images/`
  if anything references them; otherwise they're deleted.
- Alt text: posters get "Poster for <venue>, <date>" (or "Crawlspace poster, <date>" for
  orphans), and band photos get the member's name.

## Admin (Pages CMS): `.pages.yml`

- **Sidebar:** Gigs, Venues, Band, Videos, Pages (About, Merch, Contact), Site settings,
  Media.
- **Gigs view:** columns for date, venue, and title, sorted by date descending.
- **Install:** Bobby installs the Pages CMS GitHub App on the `crawlspacenh` org, not
  Ian. The installation then belongs to the org and doesn't depend on Ian's account.
- **Access:** Bobby signs in with GitHub (`feldspar88-web`). Mike, Andy, and future
  members are invited by email as collaborators and don't need GitHub accounts. Only
  GitHub users with repo access can invite or remove collaborators, which means Bobby.
- **Attribution:** `settings.commit.identity: user`, so commits carry the editor's name.
- **Undo:** every save is a Git commit and can be reverted in GitHub.

### Verified Pages CMS behavior (docs, 2026-10-10)

| Behavior                                  | Status   | Fallback if wrong in practice                        |
|-------------------------------------------|----------|------------------------------------------------------|
| TOML front matter (`toml-frontmatter`)    | Verified | YAML front matter for gigs only                      |
| Reference stores the venue slug (`{name}`) | Verified | Store `{path}`; templates take its basename         |
| Filename template uses field values       | Verified | `{year}-{month}-{day}-{primary}` with a title field  |
| Media `input` ≠ `output`                  | Verified | Images in `static/`; no resizing; Posters page lists files with `os.ReadDir` |
| Email-invited collaborators, no GitHub    | Verified | Everyone gets a GitHub account                       |
| Hosted app is free                        | Per FAQ  | Self-host on Vercel's free tier (documented option)  |
| Org installation survives Ian leaving     | Unverified | Bobby reinstalls the app; config is unaffected     |

The first implementation task is a smoke test that confirms the "Verified" rows against
the real app with a throwaway collection, before any templates are built. If the
`static/` fallback is used, the manual check "a full-size phone photo renders resized"
is dropped.

## Build, deploy, and guardrails

- **Triggers:** `.github/workflows/hugo.yaml` keeps `push` and `workflow_dispatch` and
  adds `schedule` (nightly). Deploy only runs if the Hugo build succeeds, so the last good
  site stays live after a bad edit.
- **Failure notification:** a final job runs `if: failure()`. It uses `gh` with the
  workflow token (`issues: write`) to open an issue titled "Site build failed", or comment
  on the open one, with a link to the failed run, and mentions `@feldspar88-web`. The
  issue emails Bobby, plus anyone watching the repo, including the GitHub account on the
  band Gmail. Push failures from email-invited collaborators would otherwise notify only
  the Pages CMS app, and scheduled failures would notify Ian.
- **Scheduled-workflow auto-disable:** GitHub disables scheduled workflows in public repos
  after 60 days without repository activity. During a long quiet stretch, Past Shows may
  stop updating; the JS backstop still keeps `/live.html` correct. Any CMS edit counts as
  activity. To recover, re-enable the workflow under Actions, or make any edit. The guide
  covers this.
- **Workflows:** remove `submodules: recursive` from both workflows.
- **Dependabot:** keep the `github-actions` ecosystem, which covers action major-version
  bumps. Remove the `gomod` entry, since there's no `go.mod`. Bobby merges Dependabot PRs
  once CI passes. `HUGO_VERSION` is pinned and needs an occasional manual bump. The guide
  describes both.

## Accounts and owners

| Service                            | Owner today                | Moves before Ian leaves?                                 |
|------------------------------------|----------------------------|----------------------------------------------------------|
| GitHub org `crawlspacenh`          | Ian (+ Bobby to add)       | Yes: Bobby and a band-Gmail GitHub account become owners |
| Pages CMS GitHub App               | Not installed yet          | Bobby installs it                                        |
| Formspree                          | `crawlspacenhband@gmail.com` | No change                                              |
| Google Analytics `G-42STEVR9W0`    | `crawlspacenhband@gmail.com` | No change                                              |
| Domain registration (Cloudflare Registrar) | Ian's Cloudflare   | **No**: stays with Ian for now                           |
| DNS zone `crawlspacenh.com`        | Ian's Cloudflare           | **No**: stays with Ian for now                           |
| Email Routing (`fans@`, `booking@`, `tech@`) | Ian's Cloudflare | **No**: stays with Ian for now                           |

The last three rows are one dependency on Ian's Cloudflare account. If that account
lapses, the domain renewal, the website's DNS, and booking email all stop together.
Moving them to a band-owned Cloudflare account is a follow-up, out of scope here.

## Migration

1. **Vendor the theme:** copy `hugo-split-theme` into `themes/hugo-split-theme/` as plain
   files (keep `theme = "hugo-split-theme"`), and remove the submodule and `.gitmodules`.
   Keep its `LICENSE.md` (CC BY 3.0) and the attribution comment in `hugo.toml`. Site
   overrides go in root `layouts/` and `assets/`, not edits to the theme files.
2. **Build layouts** for gigs, past shows, posters, band, videos, home "Next shows", the
   contact form partial, and the overrides for `head.html`, `intro.html`, `links.html`,
   and `split.scss`. New templates get their own CSS in one shared stylesheet. The
   remaining Markdown pages (about, merch, contact) keep their current styles moved into
   that stylesheet. No effort goes into pixel-matching what the redesign will replace.
3. **One-time migration script** in `scripts/migrate/`, deleted after cutover:
   - Parse every historical revision of `content/live.md` (history starts 2024-08-13;
     45 distinct gig dates: 4 in 2024, 20 in 2025, 21 in 2026) into gig files and a
     deduplicated venue list.
   - Match posters to gigs by date and move them to `assets/images/posters/`.
   - Convert `the-band.md` to `data/band.yml` (current lineup: Mike D'Amante, Andy
     Boeckeler, Bobby Decorte).
   - Convert the three playlist entries in `content/videos.md` to `data/videos.yml`,
     including date and description.
   - Move `params.links`, the tagline, and the background image setting into
     `data/site.yml`.
4. **Ian reviews the seeded data** and fixes venue duplicates and typos by hand.
5. Add `.pages.yml`, the nightly schedule, the failure notification, and the Dependabot
   change.
6. **Docs:** update `CLAUDE.md` and `README.md` for the new structure. Write
   `docs/editing-the-site.md`, a plain-language guide covering: add a gig, add a venue,
   upload a poster, edit the band, undo a mistake, "the site didn't update, what now"
   (check the "Site build failed" issue or the Actions tab, revert the last commit,
   re-enable the nightly workflow), and merging Dependabot PRs.

## Cutover

1. Open a PR and review the CI build. Merging to `main` deploys.
2. Bobby installs the Pages CMS GitHub App on the org, connects the repo, and invites
   Mike and Andy by email.
3. 15-minute walkthrough with Bobby: add a gig, add a venue, upload a poster, fix a typo,
   revert a change.
4. **Content the band fixes during the walkthrough:** the Contact page still says
   "a five-piece band consisting of three guitars, bass, and drums". The band writes the
   current description, and adds a share image in Site settings (today's
   `images/social.jpg` doesn't exist).
5. Apply the GitHub ownership row in [Accounts and owners](#accounts-and-owners). Ian
   removes himself from the org when he's ready.

## Testing

- Per this repo's `CLAUDE.md`, Claude doesn't run the site to test changes; Ian tests
  manually.
- **Automated:** the Hugo build in the deploy workflow on every push, with failures
  reported as issues; `pr-tests.yml` (Hugo build + htmltest) on PRs, including the
  migration PR.
- **Manual checklist for Ian:**
  - A gig dated next month appears on `/live.html` (tests `buildFuture`).
  - Gigs dated yesterday, today, and tomorrow land on the right page.
  - With no upcoming gigs, `/live.html` shows the empty message and the home page hides
    "Next shows".
  - A cancelled gig shows the badge and has `EventCancelled` structured data.
  - A gig with no poster renders cleanly.
  - Editing a venue updates every gig that uses it. Deleting a venue a gig uses leaves
    the build green and shows the slug.
  - Two gigs on the same date at the same venue get different filenames.
  - A full-size phone photo uploaded as a poster renders resized (only if media is in
    `assets/`).
  - Old URLs still resolve: `live.html`, `posters.html`, `the-band.html`, `videos.html`,
    `contact.html`, and a sample old poster, `/images/posters/2025-01-10.jpg`.
  - Nav links work from every page, including `/past-shows.html`.
  - All three video playlists embed.
  - The contact form still submits to Formspree.
  - Forcing a build failure opens a "Site build failed" issue.

## Out of scope

- **Visual redesign:** a separate spec, written after this lands.
- **Moving the domain, DNS, and Email Routing** out of Ian's Cloudflare account. This is
  a known dependency; see [Accounts and owners](#accounts-and-owners).
- **Gig history before August 2024:** only what poster filenames provide.
- **Mailing lists, ticketing, calendar feeds.**
