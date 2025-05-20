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
- Content files are stored in `/content/` directory using Markdown format
- Images are stored in `/static/images/` with subdirectories for headshots, posters, etc.
- Configuration is maintained in `hugo.toml` using TOML syntax
- The `CNAME` file in the root directory configures the custom domain for GitHub Pages

## Commands
- Build (local development): `hugo server`
- Build (production): `hugo --minify`
- Deploy: Automatic when pushed to main branch

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
- Main sections: About, The Band, Live, Videos, Posters
- Band member information: Maintained in `the-band.md` with tabular layout
- Live performances: Listed in `live.md` with chronological order
- Homepage: Main content in `_index.md`

## Special Considerations
- Maintain responsive design for optimal viewing on all devices
- Preserve the visual style consistent with the band's branding
- When adding new content, follow existing patterns and formats
- Use structured data for events and performances when possible
- For image optimization, balance quality and file size
- Ensure the CNAME file is preserved during deployments to maintain the custom domain
