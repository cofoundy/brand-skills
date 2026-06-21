#!/usr/bin/env bash
# Validate that every skill has a SKILL.md with `name:` and `description:` frontmatter,
# and that every skill listed in the marketplace manifest exists on disk (and vice versa).
set -euo pipefail
cd "$(dirname "$0")/.."

fail=0

echo "→ Validating skills/*/SKILL.md frontmatter"
for dir in skills/*/; do
  name="${dir#skills/}"; name="${name%/}"
  f="${dir}SKILL.md"
  skill_ok=1
  if [[ ! -f "$f" ]]; then
    echo "  ✗ $name: missing SKILL.md"; fail=1; continue
  fi
  if ! grep -qE '^name:' "$f"; then echo "  ✗ $name: SKILL.md missing 'name:'"; fail=1; skill_ok=0; fi
  if ! grep -qE '^description:' "$f"; then echo "  ✗ $name: SKILL.md missing 'description:'"; fail=1; skill_ok=0; fi
  [[ $skill_ok -eq 1 ]] && echo "  ✓ $name"
done

echo "→ Cross-checking marketplace manifest ↔ disk"
manifest=".claude-plugin/marketplace.json"

# Guard against the "conflicting manifests" load failure: if the marketplace entry
# lists skills explicitly while strict is not true, Claude Code refuses to load the
# plugin ("both plugin.json and marketplace entry specify components"). This is invisible
# to `claude plugin validate`, so lint it here.
if grep -qE '"skills"[[:space:]]*:' "$manifest" && ! grep -qE '"strict"[[:space:]]*:[[:space:]]*true' "$manifest"; then
  echo "  ✗ manifest lists \"skills\" explicitly but \"strict\" is not true — plugin will fail to load"; fail=1
fi

listed=$(grep -oE '"\./skills/[^"]+"' "$manifest" | sed 's|"./skills/||; s|"||')
for s in $listed; do
  [[ -d "skills/$s" ]] || { echo "  ✗ manifest lists skills/$s but it is missing on disk"; fail=1; }
done
for dir in skills/*/; do
  name="${dir#skills/}"; name="${name%/}"
  echo "$listed" | grep -qx "$name" || { echo "  ✗ skills/$name on disk but not in manifest"; fail=1; }
done

[[ $fail -eq 0 ]] && echo "✓ all skills valid" || { echo "✗ validation failed"; exit 1; }
