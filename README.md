# AsoFast landing site

A static landing site for AsoFast, an open source ASO tool for iOS and Android developers. The site is built with plain HTML, CSS, and a small Python generator. It has zero external dependencies and is designed to deploy to GitHub Pages.

## Repository structure

```
assets/             # CSS, SVG logos, favicon, screenshots
pages/              # Source HTML pages (index, privacy, terms)
blog/
  posts/            # Markdown articles with YAML frontmatter
  index.html.template   # Blog listing template
  post.html.template    # Single article template
build.py            # Static site generator (Python stdlib only)
CNAME               # GitHub Pages custom domain
robots.txt          # Crawler instructions
dist/               # Generated site (created by build.py)
```

## Build the site

Requires Python 3.11 or newer.

```bash
python3 build.py
```

This creates the `dist/` folder with the complete site, including:

- `index.html`, `privacy.html`, `terms.html`
- `blog/index.html` and `blog/{slug}/index.html` for each article
- `sitemap.xml`, `robots.txt`, `CNAME`
- All assets copied into `dist/assets/`

## Add a blog article

1. Create a new Markdown file in `blog/posts/`, for example:

```markdown
---
title: How to audit your Google Play listing
description: A practical checklist for reviewing your app listing and finding quick wins.
date: 2026-08-14
tags: google play, audit, aso
slug: how-to-audit-your-google-play-listing
---

Write your article body here using Markdown.
```

2. Run `python3 build.py`.
3. Commit the new file and the updated `dist/` folder if your deployment pipeline requires it.

## Serve locally

```bash
python3 -m http.server 8000 -d dist/
```

Then open http://localhost:8000 in your browser.

## Deploy

Deployment is handled by GitHub Actions (`.github/workflows/deploy.yml`). On every push to `main`, the workflow:

1. Checks out the repository.
2. Runs `python3 build.py`.
3. Uploads the `dist/` folder as a Pages artifact.
4. Deploys the artifact to GitHub Pages.

The custom domain `asofast.app` is configured via the `CNAME` file.

## License

The site content is part of the AsoFast project under the MIT license.
