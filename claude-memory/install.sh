#!/usr/bin/env bash
# Installs the Claude Code memory files from this directory onto the current machine:
#   CLAUDE.md            -> ~/.claude/CLAUDE.md         (global preferences)
#   rules/*.md           -> ~/claude-shared/rules/      (shared stack rules)
# Refuses to overwrite existing files unless run with --force.
set -euo pipefail

force=0
[[ "${1:-}" == "--force" ]] && force=1

src_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

install_file() {
  local src="$1" dest="$2"
  if [[ -e "$dest" && $force -eq 0 ]]; then
    if cmp -s "$src" "$dest"; then
      echo "unchanged: $dest"
    else
      echo "SKIPPED (exists, differs): $dest  -- rerun with --force to overwrite"
    fi
    return
  fi
  mkdir -p "$(dirname "$dest")"
  cp "$src" "$dest"
  echo "installed: $dest"
}

install_file "$src_dir/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
for f in "$src_dir"/rules/*.md; do
  install_file "$f" "$HOME/claude-shared/rules/$(basename "$f")"
done
