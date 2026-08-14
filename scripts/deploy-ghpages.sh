#!/usr/bin/env bash
# Build the static site and publish it to the gh-pages branch (GitHub Pages).
set -euo pipefail
cd "$(dirname "$0")/.."

python3 build.py

TMP=$(mktemp -d)
trap 'git worktree remove --force "$TMP" >/dev/null 2>&1 || true; rm -rf "$TMP"' EXIT

if git rev-parse --verify gh-pages >/dev/null 2>&1; then
  git worktree add "$TMP" gh-pages
else
  git worktree add --orphan -b gh-pages "$TMP"
fi

# Replace everything except the worktree metadata.
find "$TMP" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -a dist/. "$TMP"/

git -C "$TMP" add -A
if git -C "$TMP" diff --cached --quiet; then
  echo "No changes to deploy."
  exit 0
fi

git -C "$TMP" -c user.name="ediaStudio" -c user.email="ediaStudio@users.noreply.github.com" \
  commit -q -m "Deploy site"

ENVF="${HERMES_HOME:-$HOME/.hermes}/profiles/asofast/.env"
if [ -f "$ENVF" ] && GH=$(grep '^GITHUB_TOKEN=' "$ENVF" | head -1 | cut -d= -f2 | tr -d '\n\r') && [ -n "$GH" ]; then
  B64=$(printf "x-access-token:%s" "$GH" | base64 -w0)
  git -C "$TMP" -c http.extraheader="AUTHORIZATION: basic $B64" push -f origin gh-pages
else
  git -C "$TMP" push -f origin gh-pages
fi

echo "Deployed to gh-pages."
