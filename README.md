# Crawlspace -- The Band

[https://crawlspacenh.com]

## Editing the site

The band edits content through [Pages CMS](https://app.pagescms.org). See
[docs/editing-the-site.md](docs/editing-the-site.md). Gigs live in `content/gigs/`, everything
else editable in `data/`, and images in `assets/images/`.

## Local Development

This site is built using [Hugo](https://gohugo.io/), a fast and modern static
site generator.

### Prerequisites

- [Hugo](https://gohugo.io/installation/) (Extended version recommended)
- Git

### Getting Started

1. Clone this repository:
   ```
   git clone https://github.com/your-username/crawlspace-website.git
   cd crawlspace-website
   ```

   The theme is vendored in `themes/hugo-split-theme/`, so a plain `git clone`
   is all you need.

2. Run the Hugo development server:
   ```
   hugo server
   ```
   This will start a local development server at [http://localhost:1313/] with
   live reload enabled.

3. To see draft content during development:
   ```
   hugo server -D
   ```

4. To build the site for production:
   ```
   hugo --minify
   ```
   This will generate optimized files in the `public` directory.

### Theme Customization

This site uses the `hugo-split-theme` with custom modifications. Theme files
are located in the `/themes/hugo-split-theme/` directory.

### Adding Content

- Content files should be placed in the `/content/` directory using Markdown format
- CMS-managed images live in `/assets/images/` (posters, band, site, merch)
- Use TOML format for page front matter (+++...+++)

## Deployment

This site is deployed using GitHub Pages with a custom domain.

### GitHub Pages Configuration

1. The site is built and deployed automatically when changes are pushed to the
   main branch.
2. The custom domain `crawlspacenh.com` is configured in the `CNAME` file at
   the root of the repository.
3. DNS settings for the domain are managed externally and point to GitHub Pages
   servers.

### Manual Deployment

If you need to deploy manually:

1. Build the site:
   ```
   hugo --minify
   ```

2. Push changes to the main branch:
   ```
   git add .
   git commit -m "Update site content"
   git push origin main
   ```

GitHub Actions will automatically build and deploy the site to GitHub Pages.
