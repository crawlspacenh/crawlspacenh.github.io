# Crawlspace -- The Band

[https://crawlspacenh.com]

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

2. Initialize and update the git submodules (for themes):
   ```
   git submodule init
   git submodule update
   ```

   Or clone with submodules in one command:
   ```
   git clone --recurse-submodules https://github.com/your-username/crawlspace-website.git
   ```

3. Run the Hugo development server:
   ```
   hugo server
   ```
   This will start a local development server at [http://localhost:1313/] with
   live reload enabled.

4. To see draft content during development:
   ```
   hugo server -D
   ```

5. To build the site for production:
   ```
   hugo --minify
   ```
   This will generate optimized files in the `public` directory.

### Theme Customization

This site uses the `hugo-split-theme` with custom modifications. Theme files
are located in the `/themes/hugo-split-theme/` directory.

### Adding Content

- Content files should be placed in the `/content/` directory using Markdown format
- Images should be stored in `/static/images/` with appropriate subdirectories
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
