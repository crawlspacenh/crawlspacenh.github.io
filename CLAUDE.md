# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## General Information
- This is a static website built using Hugo
- It is hosted on GitHub Pages with a custom domain
- The base domain for the site is: `crawlspacenh.com` (defined in the CNAME file)
- The site contains content for Crawlspace, a jam band based in New Hampshire
- The band consists of five members playing various instruments
- The site uses the `hugo-split-theme` with custom modifications

## Site Structure
- Content is edited by the band through Pages CMS (`.pages.yml`). See `docs/editing-the-site.md`.
- Gigs: one front-matter-only file per show in `content/gigs/`; venues in `data/venues/*.yml`
- Band, videos, merch, site settings (tagline, background, nav links): `data/*.yml`
- CMS-managed images: `assets/images/{posters,band,site,merch}/`, referenced as `/images/...`
- Templates: root `layouts/` and `assets/` override the vendored `themes/hugo-split-theme/` (never edit the theme)
- Configuration is maintained in `hugo.toml`

## Commands
- Build (local development): `hugo server`
- Build (production): `hugo --minify`
- Deploy: automatic on push to main, plus a nightly rebuild that moves past gigs to Past Shows

## Deployment
- The site is automatically built and deployed to GitHub Pages when changes are pushed to the main branch
- Custom domain configuration is managed through the CNAME file at the root of the repository
- DNS settings for `crawlspacenh.com` are managed externally and point to GitHub Pages servers
- The site uses GitHub's automatic HTTPS for secure connections

## Style Guidelines
- Content format: Use Markdown for all content files
- HTML: Use HTML within Markdown when needed for specific formatting (tables, styling)
- Front matter: Use TOML format for page front matter (+++...+++)
- Links: Use relative URLs when linking to internal content
- Naming conventions: Use kebab-case for all file names
- Images: Include alt text for all images and appropriate ARIA attributes for HTML
- CSS: Custom styles should be included within content files when needed
- Markdown: Follow standard Markdown conventions with HTML when required

## Content Organization
- Pages: Live (upcoming gigs), Past Shows, Posters, The Band, Videos, Merch, Contact, About
- Upcoming vs. past is decided at build time by date (America/New_York) with a JS backstop

## Special Considerations
- Maintain responsive design for optimal viewing on all devices
- Preserve the visual style consistent with the band's branding
- When adding new content, follow existing patterns and formats
- Use structured data for events and performances when possible
- For image optimization, balance quality and file size
- Ensure the CNAME file is preserved during deployments to maintain the custom domain
- Never test changes made to the site; all testing will be done manually after file changes are made
