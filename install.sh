#!/usr/bin/env bash
set -euo pipefail

REPO="YashDahiwlikar914/Oh-My-Skills"
REPO_URL="https://github.com/${REPO}.git"
RAW_URL="https://raw.githubusercontent.com/${REPO}/main"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

SCOPE="project"
ALL=false
LIST_ONLY=false
DRY_RUN=false
AGENTS=()
SKILLS=()
CUSTOM_DIR=""

print_help() {
  cat <<'HELP'
Usage: install.sh [options]

Options:
  --all              Install all 26 skills without prompting
  --skill NAME       Install one skill by name, repeatable
  --agent NAME       Target harness, repeatable, default is .agents/skills
  --global           Install to user home instead of project
  --project          Install to project .agents/skills, default
  --dir PATH         Custom install directory, overrides --agent and --scope
  --list             List available skills and exit
  --dry-run          Show what would be done without copying
  --help             Show this help

Examples:
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/install.sh | bash
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/install.sh | bash -s -- --all
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/install.sh | bash -s -- --skill parallel-agents --agent claude-code --global
  ./install.sh --all --dir ~/.config/opencode/skills
HELP
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) ALL=true; shift ;;
    --skill) SKILLS+=("$2"); shift 2 ;;
    --agent) AGENTS+=("$2"); shift 2 ;;
    --global) SCOPE="global"; shift ;;
    --project) SCOPE="project"; shift ;;
    --dir) CUSTOM_DIR="$2"; shift 2 ;;
    --list) LIST_ONLY=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    --help|-h) print_help; exit 0 ;;
    *) echo "Unknown option $1"; print_help; exit 1 ;;
  esac
done

resolve_source() {
  if [[ -f "./install.sh" && -d "./parallel-agents" ]]; then
    echo "$(pwd)"
    return
  fi
  if [[ -f "$(dirname "$0")/parallel-agents/SKILL.md" ]]; then
    echo "$(dirname "$0")"
    return
  fi
  TMP=$(mktemp -d)
  echo -e "${YELLOW}Cloning ${REPO} to ${TMP}${NC}" >&2
  git clone --depth 1 --filter=blob:none "${REPO_URL}" "${TMP}" >/dev/null 2>&1
  echo "${TMP}"
}

list_available_skills() {
  local src="$1"
  for d in "${src}"/*/; do
    [[ -f "${d}SKILL.md" ]] || continue
    basename "${d}"
  done | sort
}

agent_to_path() {
  local agent="$1"
  local scope="$2"
  case "${agent}" in
    opencode)           [[ "$scope" == "global" ]] && echo "$HOME/.config/opencode/skills" || echo ".agents/skills" ;;
    claude-code|claude) [[ "$scope" == "global" ]] && echo "$HOME/.claude/skills" || echo ".claude/skills" ;;
    cursor)             [[ "$scope" == "global" ]] && echo "$HOME/.cursor/skills" || echo ".cursor/skills" ;;
    codex|openai-codex) [[ "$scope" == "global" ]] && echo "$HOME/.codex/skills" || echo ".codex/skills" ;;
    copilot|github-copilot) [[ "$scope" == "global" ]] && echo "$HOME/.copilot/skills" || echo ".github/skills" ;;
    gemini|gemini-cli)  [[ "$scope" == "global" ]] && echo "$HOME/.gemini/skills" || echo ".gemini/skills" ;;
    cline)              [[ "$scope" == "global" ]] && echo "$HOME/.cline/skills" || echo ".cline/skills" ;;
    windsurf)           [[ "$scope" == "global" ]] && echo "$HOME/.codeium/windsurf/skills" || echo ".windsurf/skills" ;;
    kilo|kilo-code)     [[ "$scope" == "global" ]] && echo "$HOME/.kilocode/skills" || echo ".kilocode/skills" ;;
    roo|roo-code)       [[ "$scope" == "global" ]] && echo "$HOME/.roo/skills" || echo ".roo/skills" ;;
    aider)              [[ "$scope" == "global" ]] && echo "$HOME/.aider/skills" || echo ".aider/skills" ;;
    augment)            [[ "$scope" == "global" ]] && echo "$HOME/.augment/skills" || echo ".augment/skills" ;;
    qwen)               [[ "$scope" == "global" ]] && echo "$HOME/.qwen/skills" || echo ".qwen/skills" ;;
    goose)              [[ "$scope" == "global" ]] && echo "$HOME/.config/goose/skills" || echo ".goose/skills" ;;
    antigravity)        [[ "$scope" == "global" ]] && echo "$HOME/.gemini/antigravity/skills" || echo ".agents/skills" ;;
    *)                  [[ "$scope" == "global" ]] && echo "$HOME/.agents/skills" || echo ".agents/skills" ;;
  esac
}

SRC=$(resolve_source)
AVAILABLE=($(list_available_skills "$SRC"))

if [[ "$LIST_ONLY" == true ]]; then
  printf "%s\n" "${AVAILABLE[@]}"
  exit 0
fi

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  if [[ "$ALL" == true ]]; then
    SKILLS=("${AVAILABLE[@]}")
  elif [[ -t 0 ]]; then
    echo "Available skills:"
    for i in "${!AVAILABLE[@]}"; do
      printf "  %2d) %s\n" $((i+1)) "${AVAILABLE[$i]}"
    done
    echo ""
    echo -e "${YELLOW}Enter numbers comma separated, or 'all'${NC}"
    read -rp "Pick skills: " PICK
    if [[ "$PICK" == "all" ]]; then
      SKILLS=("${AVAILABLE[@]}")
    else
      IFS=',' read -ra NUMS <<< "$PICK"
      for n in "${NUMS[@]}"; do
        n=$(echo "$n" | xargs)
        idx=$((n-1))
        if [[ -n "${AVAILABLE[$idx]:-}" ]]; then
          SKILLS+=("${AVAILABLE[$idx]}")
        fi
      done
    fi
  else
    echo "No --skill or --all given and no tty, listing skills"
    printf "%s\n" "${AVAILABLE[@]}"
    exit 0
  fi
fi

if [[ -n "$CUSTOM_DIR" ]]; then
  DESTS=("$CUSTOM_DIR")
else
  if [[ ${#AGENTS[@]} -eq 0 ]]; then
    if [[ -t 0 && "$SCOPE" == "project" ]]; then
      echo ""
      echo "Where to install? This covers 80+ harnesses via .agents/skills as fallback."
      echo "  1) Generic .agents/skills  - works with OpenCode, Cursor, Copilot, Codex, Gemini, Warp, and most others"
      echo "  2) Claude Code             - .claude/skills"
      echo "  3) Cursor                  - .cursor/skills"
      echo "  4) OpenCode                - .config/opencode/skills when --global"
      echo "  5) Pick specific harnesses"
      read -rp "Pick destination [1]: " DPICK
      DPICK=${DPICK:-1}
      case "$DPICK" in
        1) AGENTS=("generic") ;;
        2) AGENTS=("claude-code") ;;
        3) AGENTS=("cursor") ;;
        4) AGENTS=("opencode") ;;
        5)
          echo "Supported harnesses: opencode, claude-code, cursor, codex, copilot, gemini-cli, cline, windsurf, kilo-code, roo-code, aider, augment, qwen, goose, antigravity, generic"
          read -rp "Enter harness names comma separated: " APICK
          IFS=',' read -ra AGENTS <<< "$APICK"
          ;;
        *) AGENTS=("generic") ;;
      esac
    else
      AGENTS=("generic")
    fi
  fi
  DESTS=()
  for a in "${AGENTS[@]}"; do
    a=$(echo "$a" | xargs | tr '[:upper:]' '[:lower:]')
    [[ "$a" == "generic" ]] && a="generic"
    DESTS+=("$(agent_to_path "$a" "$SCOPE")")
  done
fi

echo ""
echo -e "${GREEN}Source${NC}  $SRC"
echo -e "${GREEN}Skills${NC}  ${SKILLS[*]}"
echo -e "${GREEN}Scope${NC}   $SCOPE"
echo -e "${GREEN}Dests${NC}   ${DESTS[*]}"
echo ""

USE_GH=false
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  if [[ -t 0 ]]; then
    read -rp "Use gh skill install when available? [y/N]: " GHANS
    [[ "$GHANS" =~ ^[Yy]$ ]] && USE_GH=true
  fi
fi

for skill in "${SKILLS[@]}"; do
  FOUND=false
  for avail in "${AVAILABLE[@]}"; do [[ "$avail" == "$skill" ]] && FOUND=true; done
  if [[ "$FOUND" == false ]]; then
    echo -e "${YELLOW}Skip unknown skill $skill${NC}"
    continue
  fi
  for dest in "${DESTS[@]}"; do
    TARGET="${dest}/${skill}"
    if [[ "$DRY_RUN" == true ]]; then
      echo "[dry-run] $skill -> $TARGET"
      continue
    fi
    if [[ "$USE_GH" == true ]]; then
      echo -e "${GREEN}Installing${NC} $skill via gh to $dest"
      gh skill install "${REPO}" "$skill" --agent generic --scope "$SCOPE" --force 2>&1 || {
        echo -e "${YELLOW}gh install failed, falling back to copy${NC}"
        mkdir -p "$TARGET"
        cp -r "${SRC}/${skill}/." "$TARGET/"
      }
    else
      echo -e "${GREEN}Copying${NC} $skill -> $TARGET"
      mkdir -p "$TARGET"
      cp -r "${SRC}/${skill}/." "$TARGET/"
    fi
  done
done

echo ""
echo -e "${GREEN}Done${NC}. Installed ${#SKILLS[@]} skill(s) to ${#DESTS[@]} location(s)."
if [[ "$SCOPE" == "project" ]]; then
  echo "Project skills live in .agents/skills and are shared by most harnesses."
  echo "Commit them if you want the team to have them."
else
  echo "Global skills are now available in every project."
fi
