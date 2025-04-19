# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## General Information
- This is a static website built using hugo
- It is hosted on github pages
- The base domain for the site is: `crawlspacenh.com`
- The site contains content for a jam band based in New Hampshire

## Commands
- Build: `hugo server` (local development server)
- Build (production): `hugo --minify`
- Deploy: Automatic when pushed to main branch

## Style Guidelines
- Content format: Use Markdown for all content files
- Content organization: Place all content in `/content/` directory
- Image assets: Store in `/static/images/` with appropriate subdirectories
- Markdown syntax: Use standard Markdown with HTML when needed for specific formatting
- Front matter: Use TOML format for page front matter
- Links: Use relative URLs when linking to internal content
- Configuration: Keep site configuration in `hugo.toml` using TOML syntax
- Naming conventions: Use kebab-case for all file names
- Accessibility: Include alt text for all images and appropriate ARIA attributes for HTML

## Theme
This site uses the `hugo-split-theme` with custom modifications. Maintain theme styling consistency when making changes.
