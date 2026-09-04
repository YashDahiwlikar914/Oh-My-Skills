#!/usr/bin/env bash
set -Eeuo pipefail

REPO="YashDahiwlikar914/Oh-My-Skills"
REPO_URL="https://github.com/${REPO}.git"

if [[ -t 1 ]]; then
  GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
else
  GREEN=""; YELLOW=""; NC=""
fi

SCOPE="project"
ALL=false
LIST_ONLY=false
DRY_RUN=false
AGENTS=()
SKILLS=()
CUSTOM_DIR=""
TMP_DIR=""

cleanup() {
  if [[ -n "${TMP_DIR}" && -d "${TMP_DIR}" ]]; then
    rm -rf -- "${TMP_DIR}"
  fi
}
trap cleanup EXIT INT TERM

printHelp() {
  cat <<'HELP'
Usage: Install.sh [options]

Options:
  --all              Install all skills without prompting
  --skill NAME       Install one skill by name, repeatable
  --agent NAME       Target harness, repeatable, default is .agents/skills
  --global           Install to user home instead of project
  --project          Install to project .agents/skills, default
  --dir PATH         Custom install directory, overrides --agent and --scope
  --list             List available skills and exit
  --dry-run          Show what would be done without copying
  --help             Show this help

Supported Agents:
  opencode, claude-code, antigravity, cursor, windsurf, copilot, codex, gemini-cli,
  cline, kilo-code, roo-code, aider, augment, qwen, goose, amp, zed, warp, trae,
  continue, pi, jetbrains, replit, bolt, factory, devin, openhands, cody, tabnine,
  supermaven, v0, lovable, vscode, neovim, firebase-studio, generic
  Use --agent multiple times for multiple harnesses. Generic is .agents/skills
  which is read by 80+ harnesses as a fallback.

Examples:
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --all
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --skill parallel-agents --agent claude-code --global
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --skill web-experience-director --agent antigravity --global
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --skill ui-ux-pro-max --agent amp --agent zed --global
  ./Install.sh --all --dir ~/.config/opencode/skills
HELP
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) ALL=true; shift ;;
    --skill)
      if [[ $# -lt 2 || "$2" == --* ]]; then echo "Missing value for --skill" >&2; exit 1; fi
      SKILLS+=("$2"); shift 2 ;;
    --agent)
      if [[ $# -lt 2 || "$2" == --* ]]; then echo "Missing value for --agent" >&2; exit 1; fi
      AGENTS+=("$2"); shift 2 ;;
    --global) SCOPE="global"; shift ;;
    --project) SCOPE="project"; shift ;;
    --dir)
      if [[ $# -lt 2 || "$2" == --* ]]; then echo "Missing value for --dir" >&2; exit 1; fi
      CUSTOM_DIR="$2"; shift 2 ;;
    --list) LIST_ONLY=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    --help|-h) printHelp; exit 0 ;;
    *) echo "Unknown option $1" >&2; printHelp; exit 1 ;;
  esac
done

resolveSource() {
  if [[ -f "./Install.sh" && -d "./parallel-agents" ]]; then
    echo "$(pwd)"
    return
  fi
  if [[ -f "./install.sh" && -d "./parallel-agents" ]]; then
    echo "$(pwd)"
    return
  fi
  local selfDir
  selfDir="$(dirname -- "$0")"
  if [[ -f "${selfDir}/parallel-agents/SKILL.md" ]]; then
    echo "${selfDir}"
    return
  fi
  if ! command -v git >/dev/null 2>&1; then
    echo "git is required to fetch skills" >&2; exit 1
  fi
  TMP_DIR="$(mktemp -d)"
  printf "%bCloning %s to %s%b\n" "${YELLOW}" "${REPO}" "${TMP_DIR}" "${NC}" >&2
  git clone --depth 1 --filter=blob:none "${REPO_URL}" "${TMP_DIR}" >/dev/null 2>&1
  echo "${TMP_DIR}"
}

listAvailableSkills() {
  local src="$1"
  local d
  for d in "${src}"/*/; do
    [[ -f "${d}SKILL.md" ]] || continue
    basename -- "${d%/}"
  done | sort
}

validateSkillName() {
  [[ "$1" =~ ^[a-z0-9][a-z0-9-]*$ ]]
}

isSafePath() {
  local p="$1"
  [[ -n "$p" ]] && [[ "$p" != "/" ]] && [[ "$p" != "$HOME" ]]
}

agentToPath() {
  local agent="$1"
  local scope="$2"
  case "${agent}" in
    opencode)             [[ "$scope" == "global" ]] && echo "$HOME/.config/opencode/skills" || echo ".agents/skills" ;;
    claude-code|claude|anthropic)   [[ "$scope" == "global" ]] && echo "$HOME/.claude/skills" || echo ".claude/skills" ;;
    cursor|cursor-ide)               [[ "$scope" == "global" ]] && echo "$HOME/.cursor/skills" || echo ".cursor/skills" ;;
    codex|openai-codex|openai)   [[ "$scope" == "global" ]] && echo "$HOME/.codex/skills" || echo ".codex/skills" ;;
    copilot|github-copilot|github) [[ "$scope" == "global" ]] && echo "$HOME/.copilot/skills" || echo ".github/skills" ;;
    gemini|gemini-cli|google-gemini)    [[ "$scope" == "global" ]] && echo "$HOME/.gemini/skills" || echo ".gemini/skills" ;;
    antigravity|antigravity-ide|google-antigravity) [[ "$scope" == "global" ]] && echo "$HOME/.config/antigravity/skills" || echo ".antigravity/skills" ;;
    cline)                [[ "$scope" == "global" ]] && echo "$HOME/.cline/skills" || echo ".cline/skills" ;;
    windsurf|windsurf-ide|codeium-windsurf|codeium)             [[ "$scope" == "global" ]] && echo "$HOME/.codeium/windsurf/skills" || echo ".windsurf/skills" ;;
    kilo|kilo-code)       [[ "$scope" == "global" ]] && echo "$HOME/.kilocode/skills" || echo ".kilocode/skills" ;;
    roo|roo-code)         [[ "$scope" == "global" ]] && echo "$HOME/.roo/skills" || echo ".roo/skills" ;;
    aider)                [[ "$scope" == "global" ]] && echo "$HOME/.aider/skills" || echo ".aider/skills" ;;
    augment)              [[ "$scope" == "global" ]] && echo "$HOME/.augment/skills" || echo ".augment/skills" ;;
    qwen|qwen-code|alibaba-qwen)                 [[ "$scope" == "global" ]] && echo "$HOME/.qwen/skills" || echo ".qwen/skills" ;;
    goose)                [[ "$scope" == "global" ]] && echo "$HOME/.config/goose/skills" || echo ".goose/skills" ;;
    amp|ampcode|sourcegraph-amp)          [[ "$scope" == "global" ]] && echo "$HOME/.config/amp/skills" || echo ".amp/skills" ;;
    zed)                  [[ "$scope" == "global" ]] && echo "$HOME/.config/zed/skills" || echo ".zed/skills" ;;
    warp)                 [[ "$scope" == "global" ]] && echo "$HOME/.warp/skills" || echo ".warp/skills" ;;
    trae|trae-ide|bytedance-trae)        [[ "$scope" == "global" ]] && echo "$HOME/.config/trae/skills" || echo ".trae/skills" ;;
    continue|continue-dev)                [[ "$scope" == "global" ]] && echo "$HOME/.continue/skills" || echo ".continue/skills" ;;
    pi|pi-agent)          [[ "$scope" == "global" ]] && echo "$HOME/.pi/agent/skills" || echo ".pi/skills" ;;
    jetbrains|jetbrains-ai|junie) [[ "$scope" == "global" ]] && echo "$HOME/.config/JetBrains/skills" || echo ".jetbrains/skills" ;;
    replit|replit-agent) [[ "$scope" == "global" ]] && echo "$HOME/.config/replit/skills" || echo ".replit/skills" ;;
    bolt|stackblitz|bolt-diy) [[ "$scope" == "global" ]] && echo "$HOME/.config/bolt/skills" || echo ".bolt/skills" ;;
    factory|droid|factory-droid) [[ "$scope" == "global" ]] && echo "$HOME/.factory/skills" || echo ".factory/skills" ;;
    devin|cognition-devin) [[ "$scope" == "global" ]] && echo "$HOME/.config/devin/skills" || echo ".devin/skills" ;;
    openhands|all-hands) [[ "$scope" == "global" ]] && echo "$HOME/.openhands/skills" || echo ".openhands/skills" ;;
    cody|sourcegraph-cody) [[ "$scope" == "global" ]] && echo "$HOME/.config/cody/skills" || echo ".cody/skills" ;;
    tabnine) [[ "$scope" == "global" ]] && echo "$HOME/.tabnine/skills" || echo ".tabnine/skills" ;;
    supermaven) [[ "$scope" == "global" ]] && echo "$HOME/.supermaven/skills" || echo ".supermaven/skills" ;;
    v0|vercel-v0) [[ "$scope" == "global" ]] && echo "$HOME/.config/v0/skills" || echo ".v0/skills" ;;
    lovable) [[ "$scope" == "global" ]] && echo "$HOME/.config/lovable/skills" || echo ".lovable/skills" ;;
    vscode|vs-code|code) [[ "$scope" == "global" ]] && echo "$HOME/.vscode/skills" || echo ".vscode/skills" ;;
    neovim|nvim|avante) [[ "$scope" == "global" ]] && echo "$HOME/.config/nvim/skills" || echo ".nvim/skills" ;;
    firebase-studio|firebase) [[ "$scope" == "global" ]] && echo "$HOME/.config/firebase/studio/skills" || echo ".firebase/skills" ;;
    *)                    [[ "$scope" == "global" ]] && echo "$HOME/.agents/skills" || echo ".agents/skills" ;;
  esac
}

SRC="$(resolveSource)"
mapfile -t AVAILABLE < <(listAvailableSkills "$SRC")

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
    printf "%bEnter numbers comma separated, or 'all'%b\n" "${YELLOW}" "${NC}"
    read -rp "Pick skills: " PICK || PICK=""
    if [[ "$PICK" == "all" ]]; then
      SKILLS=("${AVAILABLE[@]}")
    else
      IFS=',' read -ra NUMS <<< "$PICK"
      for n in "${NUMS[@]}"; do
        n="$(echo "$n" | xargs)"
        [[ "$n" =~ ^[0-9]+$ ]] || continue
        idx=$((n-1))
        if [[ -n "${AVAILABLE[$idx]:-}" ]]; then
          SKILLS+=("${AVAILABLE[$idx]}")
        fi
      done
    fi
  else
    echo "No --skill or --all given and no tty, listing skills" >&2
    printf "%s\n" "${AVAILABLE[@]}"
    exit 0
  fi
fi

for s in "${SKILLS[@]}"; do
  if ! validateSkillName "$s"; then
    echo "Invalid skill name $s" >&2; exit 1
  fi
done

if [[ -n "$CUSTOM_DIR" ]]; then
  if ! isSafePath "$CUSTOM_DIR"; then
    echo "Refusing unsafe custom dir $CUSTOM_DIR" >&2; exit 1
  fi
  DESTS=("$CUSTOM_DIR")
else
  if [[ ${#AGENTS[@]} -eq 0 ]]; then
    if [[ -t 0 && "$SCOPE" == "project" ]]; then
      echo ""
      echo "Where to install? Generic .agents/skills works with 80+ harnesses as fallback."
      echo "  1) Generic .agents/skills   - works with OpenCode, Warp, and most others"
      echo "  2) Claude Code              - .claude/skills"
      echo "  3) Antigravity IDE          - .antigravity/skills"
      echo "  4) Cursor                   - .cursor/skills"
      echo "  5) Windsurf                 - .codeium/windsurf/skills"
      echo "  6) GitHub Copilot           - .github/skills"
      echo "  7) OpenCode                 - .config/opencode/skills when --global"
      echo "  8) Gemini CLI               - .gemini/skills"
      echo "  9) Pick specific harnesses"
      read -rp "Pick destination [1]: " DPICK || DPICK=""
      DPICK=${DPICK:-1}
      case "$DPICK" in
        1) AGENTS=("generic") ;;
        2) AGENTS=("claude-code") ;;
        3) AGENTS=("antigravity") ;;
        4) AGENTS=("cursor") ;;
        5) AGENTS=("windsurf") ;;
        6) AGENTS=("copilot") ;;
        7) AGENTS=("opencode") ;;
        8) AGENTS=("gemini-cli") ;;
        9)
          echo "Supported harnesses: opencode, claude-code, antigravity, cursor, windsurf, copilot, codex, gemini-cli, cline, kilo-code, roo-code, aider, augment, qwen, goose, amp, zed, warp, trae, continue, pi, jetbrains, replit, bolt, factory, devin, openhands, cody, tabnine, generic"
          read -rp "Enter harness names comma separated: " APICK || APICK=""
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
    a="$(echo "$a" | xargs | tr '[:upper:]' '[:lower:]')"
    if [[ "$a" == "generic" ]]; then
      a="generic"
    fi
    DESTS+=("$(agentToPath "$a" "$SCOPE")")
  done
fi

printf "\n%bSource%b  %s\n" "${GREEN}" "${NC}" "$SRC"
printf "%bSkills%b  %s\n" "${GREEN}" "${NC}" "${SKILLS[*]}"
printf "%bScope%b   %s\n" "${GREEN}" "${NC}" "$SCOPE"
printf "%bDests%b   %s\n" "${GREEN}" "${NC}" "${DESTS[*]}"
printf "\n"

USE_GH=false
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  if [[ -t 0 ]]; then
    read -rp "Use gh skill install when available? [y/N]: " GHANS || GHANS=""
    [[ "$GHANS" =~ ^[Yy]$ ]] && USE_GH=true
  fi
fi

for skill in "${SKILLS[@]}"; do
  FOUND=false
  for avail in "${AVAILABLE[@]}"; do
    if [[ "$avail" == "$skill" ]]; then FOUND=true; break; fi
  done
  if [[ "$FOUND" == false ]]; then
    printf "%bSkip unknown skill %s%b\n" "${YELLOW}" "$skill" "${NC}"
    continue
  fi
  for dest in "${DESTS[@]}"; do
    TARGET="${dest}/${skill}"
    if [[ "$DRY_RUN" == true ]]; then
      echo "[dry-run] $skill -> $TARGET"
      continue
    fi
    if [[ "$USE_GH" == true ]]; then
      printf "%bInstalling%b %s via gh to %s\n" "${GREEN}" "${NC}" "$skill" "$dest"
      if ! gh skill install "${REPO}" "$skill" --agent generic --scope "$SCOPE" --force 2>&1; then
        printf "%bgh install failed, falling back to copy%b\n" "${YELLOW}" "${NC}"
        mkdir -p -- "$TARGET"
        cp -r -- "${SRC}/${skill}/." "$TARGET/"
      fi
    else
      printf "%bCopying%b %s -> %s\n" "${GREEN}" "${NC}" "$skill" "$TARGET"
      mkdir -p -- "$TARGET"
      cp -r -- "${SRC}/${skill}/." "$TARGET/"
    fi
  done
done

printf "\n%bDone%b. Installed %d skill(s) to %d location(s).\n" "${GREEN}" "${NC}" "${#SKILLS[@]}" "${#DESTS[@]}"
if [[ "$SCOPE" == "project" ]]; then
  echo "Project skills live in .agents/skills and are shared by most harnesses."
  echo "Commit them if you want the team to have them."
else
  echo "Global skills are now available in every project."
fi
