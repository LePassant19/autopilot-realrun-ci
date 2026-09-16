#!/usr/bin/env bash
# Preuve exécutable d'AC3 (STORY-009) : seuls CANARY.md et tests/test_canary.py
# diffèrent de `main`. Sort non-nul (et liste les coupables) si un autre fichier
# — notamment pyproject.toml ou uv.lock — a été modifié, ajouté ou supprimé.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

base_commit="$(git merge-base HEAD main)"

# `git diff --name-only <base>` (un seul ref) compare `<base>` à l'état courant
# de l'arbre de travail : ça capte aussi bien les commits faits depuis la base
# que les modifications non commitées, pour les fichiers déjà suivis par git.
mapfile -t changed_files < <(git diff --name-only "$base_commit" -- .)

allowed_files=("CANARY.md" "tests/test_canary.py")

violations=()
for f in "${changed_files[@]}"; do
  [ -z "$f" ] && continue
  is_allowed=0
  for a in "${allowed_files[@]}"; do
    if [ "$f" = "$a" ]; then
      is_allowed=1
      break
    fi
  done
  if [ "$is_allowed" -eq 0 ]; then
    violations+=("$f")
  fi
done

if [ "${#violations[@]}" -gt 0 ]; then
  echo "AC3 FAIL: fichier(s) hors périmètre modifié(s) depuis $base_commit :" >&2
  printf '  - %s\n' "${violations[@]}" >&2
  exit 1
fi

echo "AC3 OK: seul CANARY.md et/ou tests/test_canary.py diffèrent de main (base $base_commit)"
exit 0
