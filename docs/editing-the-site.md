# How to update the Crawlspace website

You edit the site at **https://app.pagescms.org**. Sign in (Bobby: with GitHub; everyone
else: with the email invite), pick **crawlspacenh.github.io**, and use the menu on the left.
Every time you press **Save**, the site rebuilds itself. Changes are live in about two minutes.

## Add a gig
1. **Gigs** → **Add an entry**.
2. Fill in **Date**, **Start time** (like `6 pm`), and pick the **Venue**.
3. Optional: end time, event name, poster, ticket link, notes.
4. **Save**.

Past gigs move to the Past Shows page on their own the morning after. Don't delete them.

## Cancel a gig
Open the gig, tick **Cancelled**, and **Save**. It stays listed with a "Cancelled" badge.

## Add a venue
If a venue isn't in the dropdown: **Venues** → **Add an entry**. Fill in the name and address.
For the map link, use Google Maps → Share → Copy link. Then go back and add the gig.
Don't delete a venue that old gigs use; just leave it.

## Upload a poster
In a gig, click **Poster** → upload the image straight from your phone. Big photos are fine.
It shows up on the gig and on the Posters page.

## Edit the band, videos, merch, or site settings
Use **Band**, **Videos**, **Merch**, or **Site settings**. Drag items to reorder them.
For videos, paste the YouTube link from the Share button. Video and playlist links both work.

## Undo a mistake
Every save is recorded. On GitHub, open the repository → **Commits**, find your change, and
ask Bobby to revert it, or just fix it in Pages CMS and save again.

## The site didn't update
1. Check GitHub for an open issue called **"Site build failed"**. It links to what went wrong.
2. Usually the last save caused it. Fix or undo that change in Pages CMS. The next save
   rebuilds the site. Close the issue once the site is updated.
3. Nothing in Pages CMS for a couple of months? GitHub pauses the nightly rebuild in quiet
   repos. Go to **Actions** → **Deploy Hugo site to Pages** → **Enable workflow**, or just
   save any change.

While a build is failing, the old version of the site stays up. Nothing is ever lost.

## For Bobby: keeping it running
- **Dependabot PRs** ("chore(deps): bump actions/..."): merge them when the checks are green.
- **Hugo version**: `HUGO_VERSION` in `.github/workflows/hugo.yaml` and `pr-tests.yml`.
  Bump it about once a year; if the PR checks pass, merge.
- **Inviting people**: Pages CMS → the repo → **Collaborators** → invite by email.
