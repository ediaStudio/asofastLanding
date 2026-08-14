#!/usr/bin/env python3
"""Build the static AsoFast landing site.

Usage:
    python3 build.py

Outputs the site into `dist/` and prints a short summary.
"""

from __future__ import annotations

import datetime
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS_DIR = ROOT / "blog" / "posts"
PAGES_DIR = ROOT / "pages"
BLOG_DIR = ROOT / "blog"
ASSETS_DIR = ROOT / "assets"
DIST_DIR = ROOT / "dist"

SITE_URL = "https://asofast.app"
REPO_URL = "https://github.com/ediaStudio/asofast"
EMAIL = "contact@asofast.app"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
UL_ITEM_RE = re.compile(r"^([\*\-])\s+(.*)$")
OL_ITEM_RE = re.compile(r"^(\d+)\.\s+(.*)$")
CODE_BLOCK_RE = re.compile(r"^```(.*)$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")


def die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def format_size(num_bytes: int) -> str:
    for unit in ("B", "KB", "MB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} GB"


def parse_frontmatter(content: str, filename: str) -> dict:
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError(f"{filename}: missing or invalid frontmatter")

    fm_text, body = match.groups()
    data: dict[str, str | list[str]] = {}
    for line in fm_text.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key == "tags":
            value = value.strip("[]")
            data[key] = [tag.strip() for tag in value.split(",") if tag.strip()]
        else:
            data[key] = value

    required = {"title", "description", "date", "tags", "slug"}
    missing = required - set(data.keys())
    if missing:
        raise ValueError(f"{filename}: missing frontmatter keys: {', '.join(sorted(missing))}")

    try:
        datetime.datetime.strptime(str(data["date"]), "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{filename}: invalid date '{data['date']}' (expected YYYY-MM-DD)") from exc

    data["body"] = body
    return data


def inline_html(text: str) -> str:
    """Convert inline Markdown to HTML."""
    # Protect inline code spans so their contents are escaped literally.
    codes: list[str] = []

    def stash_code(match: re.Match) -> str:
        codes.append(html.escape(match.group(1)))
        return f"__CODE_{len(codes) - 1}__"

    text = INLINE_CODE_RE.sub(stash_code, text)
    text = html.escape(text)
    text = BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = ITALIC_RE.sub(r"<em>\1</em>", text)
    text = LINK_RE.sub(r'<a href="\2">\1</a>', text)

    for idx, code in enumerate(codes):
        text = text.replace(f"__CODE_{idx}__", f"<code>{code}</code>")
    return text


def markdown_to_html(md: str) -> str:
    """A small Markdown-to-HTML converter.

    Supports headings, paragraphs, unordered/ordered lists, links, bold,
    italic, inline code, and fenced code blocks.
    """
    lines = md.splitlines()
    output: list[str] = []
    in_code = False
    code_buffer: list[str] = []
    code_lang = ""
    in_ul = False
    in_ol = False
    para_buffer: list[str] = []

    def flush_para() -> None:
        nonlocal para_buffer
        if para_buffer:
            joined = " ".join(para_buffer).strip()
            if joined:
                output.append(f"<p>{inline_html(joined)}</p>")
            para_buffer = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            output.append("</ul>")
            in_ul = False
        if in_ol:
            output.append("</ol>")
            in_ol = False

    for raw_line in lines:
        line = raw_line.rstrip()

        if in_code:
            if line.strip() == "```":
                code_text = "\n".join(code_buffer)
                escaped = html.escape(code_text)
                header = f'<div class="code-header">{html.escape(code_lang)}</div>' if code_lang else ""
                output.append(f"{header}<pre><code>{escaped}</code></pre>")
                code_buffer = []
                code_lang = ""
                in_code = False
            else:
                code_buffer.append(raw_line)
            continue

        code_fence = CODE_BLOCK_RE.match(line)
        if code_fence:
            flush_para()
            close_lists()
            code_lang = code_fence.group(1).strip()
            in_code = True
            continue

        heading = HEADING_RE.match(line)
        if heading:
            flush_para()
            close_lists()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            output.append(f"<h{level}>{inline_html(text)}</h{level}>")
            continue

        ul_match = UL_ITEM_RE.match(line)
        if ul_match:
            flush_para()
            if in_ol:
                output.append("</ol>")
                in_ol = False
            if not in_ul:
                output.append("<ul>")
                in_ul = True
            output.append(f"<li>{inline_html(ul_match.group(2))}</li>")
            continue

        ol_match = OL_ITEM_RE.match(line)
        if ol_match:
            flush_para()
            if in_ul:
                output.append("</ul>")
                in_ul = False
            if not in_ol:
                output.append("<ol>")
                in_ol = True
            output.append(f"<li>{inline_html(ol_match.group(2))}</li>")
            continue

        if line.strip() == "":
            flush_para()
            close_lists()
            continue

        # Regular paragraph line.
        close_lists()
        para_buffer.append(line)

    flush_para()
    close_lists()
    return "\n".join(output)


def apply_vars(text: str, variables: dict[str, str]) -> str:
    for key, value in variables.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def build_post_card(post: dict) -> str:
    tags_html = "".join(f'<span class="blog-tag">{html.escape(tag)}</span>' for tag in post["tags"])
    return (
        f'<article class="blog-card">\n'
        f'  <a href="/blog/{post["slug"]}/">\n'
        f'    <time datetime="{post["date"]}">{post["date"]}</time>\n'
        f'    <h2>{html.escape(post["title"])}</h2>\n'
        f'    <p>{html.escape(post["description"])}</p>\n'
        f'    <div class="blog-tags">{tags_html}</div>\n'
        f'  </a>\n'
        f'</article>'
    )


def build_json_ld(post: dict) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": post["date"],
        "dateModified": post["date"],
        "author": {"@type": "Organization", "name": "AsoFast"},
        "publisher": {"@type": "Organization", "name": "AsoFast"},
        "url": f"{SITE_URL}/blog/{post['slug']}/",
    }
    return f'<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>'


def load_posts() -> list[dict]:
    if not POSTS_DIR.exists():
        return []
    posts: list[dict] = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
            post = parse_frontmatter(content, path.name)
            post["content_html"] = markdown_to_html(post["body"])
            posts.append(post)
        except ValueError as exc:
            die(str(exc))
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def build() -> None:
    year = str(datetime.datetime.now().year)
    global_vars = {
        "YEAR": year,
        "REPO_URL": REPO_URL,
        "SITE_URL": SITE_URL,
        "EMAIL": EMAIL,
    }

    posts = load_posts()

    # Clean and recreate dist.
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    # Copy assets.
    shutil.copytree(ASSETS_DIR, DIST_DIR / "assets")

    # Build pages from /pages.
    for page_path in PAGES_DIR.glob("*.html"):
        content = page_path.read_text(encoding="utf-8")
        content = apply_vars(content, global_vars)
        (DIST_DIR / page_path.name).write_text(content, encoding="utf-8")

    # Also create clean URL folders for privacy and terms.
    (DIST_DIR / "privacy").mkdir()
    (DIST_DIR / "privacy" / "index.html").write_text(
        apply_vars((PAGES_DIR / "privacy.html").read_text(encoding="utf-8"), global_vars),
        encoding="utf-8",
    )
    (DIST_DIR / "terms").mkdir()
    (DIST_DIR / "terms" / "index.html").write_text(
        apply_vars((PAGES_DIR / "terms.html").read_text(encoding="utf-8"), global_vars),
        encoding="utf-8",
    )

    # Build blog index.
    blog_index_template = (BLOG_DIR / "index.html.template").read_text(encoding="utf-8")
    posts_html = "\n".join(build_post_card(post) for post in posts)
    index_vars = {**global_vars, "POSTS": posts_html}
    blog_index = apply_vars(blog_index_template, index_vars)
    (DIST_DIR / "blog").mkdir()
    (DIST_DIR / "blog" / "index.html").write_text(blog_index, encoding="utf-8")

    # Build individual posts.
    post_template = (BLOG_DIR / "post.html.template").read_text(encoding="utf-8")
    for post in posts:
        post_vars = {
            **global_vars,
            "TITLE": html.escape(post["title"]),
            "DESCRIPTION": html.escape(post["description"]),
            "DATE": post["date"],
            "SLUG": post["slug"],
            "CONTENT": post["content_html"],
            "JSON_LD": build_json_ld(post),
        }
        post_html = apply_vars(post_template, post_vars)
        post_dir = DIST_DIR / "blog" / post["slug"]
        post_dir.mkdir(parents=True)
        (post_dir / "index.html").write_text(post_html, encoding="utf-8")

    # Sitemap.
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    urls = [
        ("https://asofast.app/", today, "weekly", "1.0"),
        ("https://asofast.app/blog/", today, "weekly", "0.8"),
    ]
    for post in posts:
        urls.append((
            f"https://asofast.app/blog/{post['slug']}/",
            post["date"],
            "monthly",
            "0.7",
        ))
    urls.extend([
        ("https://asofast.app/privacy/", today, "yearly", "0.3"),
        ("https://asofast.app/terms/", today, "yearly", "0.3"),
    ])
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, changefreq, priority in urls:
        sitemap_lines.append("  <url>")
        sitemap_lines.append(f"    <loc>{loc}</loc>")
        sitemap_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        sitemap_lines.append(f"    <changefreq>{changefreq}</changefreq>")
        sitemap_lines.append(f"    <priority>{priority}</priority>")
        sitemap_lines.append("  </url>")
    sitemap_lines.append("</urlset>")
    (DIST_DIR / "sitemap.xml").write_text("\n".join(sitemap_lines) + "\n", encoding="utf-8")

    # Robots.
    (DIST_DIR / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://asofast.app/sitemap.xml\n",
        encoding="utf-8",
    )

    # CNAME.
    (DIST_DIR / "CNAME").write_text("asofast.app", encoding="utf-8")

    # Summary.
    total_pages = sum(1 for _ in DIST_DIR.rglob("*.html"))
    total_assets = sum(1 for _ in DIST_DIR.rglob("*") if _.is_file() and _.suffix != ".html")
    total_size = sum(f.stat().st_size for f in DIST_DIR.rglob("*") if f.is_file())

    print("Build complete.")
    print(f"  Articles generated: {len(posts)}")
    print(f"  HTML pages:         {total_pages}")
    print(f"  Asset files:        {total_assets}")
    print(f"  Total dist size:    {format_size(total_size)}")


if __name__ == "__main__":
    build()
