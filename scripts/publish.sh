#!/usr/bin/env bash
# Publica dist/ en la rama gh-pages del repositorio (GitHub Pages).
# Requiere: gh autenticado y repo existente.
set -euo pipefail

REPO="${GITHUB_REPO:-ray86-dev/camisetas-interinos}"
cd "$(dirname "$0")/.."

echo "→ Generando dist/"
python build.py --check

echo "→ Publicando en la rama gh-pages de $REPO"
TMP="$(mktemp -d)"
cp -r dist/. "$TMP/"
touch "$TMP/.nojekyll"
(
  cd "$TMP"
  git init -q -b gh-pages
  git add -A
  git -c user.name="Llamamiento 23:59" -c user.email="deploy@local" commit -qm "publica tienda $(date -u +%FT%TZ)"
  git push -f "https://github.com/$REPO.git" gh-pages
)
rm -rf "$TMP"
echo "→ Listo: https://${REPO%%/*}.github.io/${REPO##*/}/"
