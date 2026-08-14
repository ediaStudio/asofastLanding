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
3. Deploy (see below).

## Serve locally

```bash
python3 -m http.server 8000 -d dist/
```

Then open http://localhost:8000 in your browser.

## Deploy

The site is served from the `gh-pages` branch of this repository. To build and
publish in one step:

```bash
./scripts/deploy-ghpages.sh
```

The script runs `python3 build.py`, replaces the `gh-pages` branch content with
`dist/`, and force-pushes it. If a `GITHUB_TOKEN` is available in the Hermes
profile environment file it is used for the push; otherwise your normal git
credentials are used.

The custom domain `asofast.app` is configured via the `CNAME` file (GitHub
Pages picks it up automatically on the `gh-pages` branch).

> Note: `.github/workflows/deploy.yml` (GitHub Actions deployment) is kept in
> the repo for later use but is currently not committed, because the current
> GitHub token lacks the `workflow` scope. Once the token has that scope, add
> the file back and switch Pages to "Deploy from a branch: GitHub Actions".

## License

The site content is part of the AsoFast project under the MIT license.
