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
Usage: Install.sh [Options]

Options:
  --all              Install All Skills Without Prompting
  --skill NAME       Install One Skill By Name, Repeatable
  --agent NAME       Target Harness, Repeatable, Default Is .agents/skills
  --global           Install To User Home Instead Of Project
  --project          Install To Project .agents/skills, Default
  --dir PATH         Custom Install Directory, Overrides --agent And --scope
  --list             List Available Skills And Exit
  --dry-run          Show What Would Be Done Without Copying
  --help             Show This Help

Supported Agents:
  claude-code, opencode, codex, copilot, gemini-cli, antigravity, cursor,
  windsurf, cline, kilo-code, roo-code, amp, zed, warp, trae, pi, jetbrains,
  replit, factory, devin, openhands, goose, augment, qwen, generic
  Paths Are Verified Against Each Vendor's Official Docs. Generic Is
  .agents/skills, Which Most Harnesses Read Too. Use --agent Multiple
  Times For Multiple Harnesses.
  Aider And Continue Have No Skills Support, So They Are Not Listed.

Examples:
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --all
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --skill parallel-agents --agent claude-code --global
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --skill web-experience-director --agent antigravity --global
  curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --skill ui-ux-pro-max --agent amp --agent zed --global
  ./Install.sh --all --dir ~/.config/opencode/skills
HELP
}

needValue() {
  if [[ $# -lt 2 || "$2" == --* ]]; then
    echo "Missing Value For $1" >&2
    exit 1
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) ALL=true; shift ;;
    --skill) needValue "$@"; SKILLS+=("$2"); shift 2 ;;
    --agent) needValue "$@"; AGENTS+=("$2"); shift 2 ;;
    --global) SCOPE="global"; shift ;;
    --project) SCOPE="project"; shift ;;
    --dir) needValue "$@"; CUSTOM_DIR="$2"; shift 2 ;;
    --list) LIST_ONLY=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    --help|-h) printHelp; exit 0 ;;
    *) echo "Unknown Option $1" >&2; printHelp; exit 1 ;;
  esac
done

resolveSource() {
  # Local copy wins when this file sits next to the skill folders.
  if { [[ -f ./Install.sh ]] || [[ -f ./install.sh ]]; } && [[ -d ./parallel-agents ]]; then
    pwd
    return
  fi
  local selfDir
  selfDir="$(dirname -- "$0")"
  if [[ -f "${selfDir}/parallel-agents/SKILL.md" ]]; then
    echo "${selfDir}"
    return
  fi
  if ! command -v git >/dev/null 2>&1; then
    echo "Git Is Required To Fetch Skills" >&2; exit 1
  fi
  TMP_DIR="$(mktemp -d)"
  printf "%bCloning %s To %s%b\n" "${YELLOW}" "${REPO}" "${TMP_DIR}" "${NC}" >&2
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
  # Paths verified against official docs (Sep 2026):
  # claude: code.claude.com/docs/en/skills
  # opencode: opencode.ai/docs/skills
  # cursor: cursor.com/docs/context/skills
  # codex: developers.openai.com/codex (.agents/skills only, not .codex/skills)
  # copilot: docs.github.com/en/copilot/concepts/agents/about-agent-skills
  # gemini: github.com/google-gemini/gemini-cli docs/cli/skills.md
  # antigravity: antigravity.google/docs/skills
  # windsurf: docs.windsurf.com/windsurf/cascade/skills
  # cline: docs.cline.bot/features/skills
  # kilo: kilo.ai/docs/features/skills
  # roo: docs.roocode.com/features/skills
  # amp: ampcode.com/docs/customize/skills
  # zed: zed.dev/docs/ai/skills (.agents/skills only)
  # warp: docs.warp.dev/agents/capabilities/skills
  # trae: docs.trae.ai/ide/skills
  # pi: github.com/earendil-works/pi docs/skills.md
  # junie: junie.jetbrains.com/docs/agent-skills.html
  # replit: docs.replit.com/features/agent/skills (project only)
  # droid: docs.factory.ai/harness/skills
  # devin: docs.devin.ai/cli/extensibility/skills
  # openhands: docs.openhands.dev/overview/skills.md
  # goose: goose-docs.ai/docs/guides/context-engineering/using-skills
  # augment: docs.augmentcode.com/cli/skills.md
  # qwen: qwenlm.github.io/qwen-code-docs users/features/skills
  local agent="$1"
  local scope="$2"
  case "${agent}" in
    claude-code|claude|anthropic)
      [[ "$scope" == "global" ]] && echo "$HOME/.claude/skills" || echo ".claude/skills" ;;
    opencode)
      [[ "$scope" == "global" ]] && echo "$HOME/.config/opencode/skills" || echo ".opencode/skills" ;;
    codex|openai-codex|openai)
      [[ "$scope" == "global" ]] && echo "$HOME/.agents/skills" || echo ".agents/skills" ;;
    copilot|github-copilot|github|vscode)
      [[ "$scope" == "global" ]] && echo "$HOME/.copilot/skills" || echo ".github/skills" ;;
    gemini|gemini-cli|google-gemini)
      [[ "$scope" == "global" ]] && echo "$HOME/.gemini/skills" || echo ".gemini/skills" ;;
    antigravity|antigravity-ide|google-antigravity|firebase)
      [[ "$scope" == "global" ]] && echo "$HOME/.gemini/config/skills" || echo ".agents/skills" ;;
    cursor|cursor-ide)
      [[ "$scope" == "global" ]] && echo "$HOME/.cursor/skills" || echo ".cursor/skills" ;;
    windsurf|windsurf-ide|codeium|codeium-windsurf)
      [[ "$scope" == "global" ]] && echo "$HOME/.codeium/windsurf/skills" || echo ".windsurf/skills" ;;
    cline)
      [[ "$scope" == "global" ]] && echo "$HOME/.cline/skills" || echo ".cline/skills" ;;
    kilo|kilo-code)
      [[ "$scope" == "global" ]] && echo "$HOME/.kilo/skills" || echo ".kilo/skills" ;;
    roo|roo-code)
      [[ "$scope" == "global" ]] && echo "$HOME/.roo/skills" || echo ".roo/skills" ;;
    amp|ampcode|sourcegraph-amp)
      [[ "$scope" == "global" ]] && echo "$HOME/.config/agents/skills" || echo ".agents/skills" ;;
    zed)
      [[ "$scope" == "global" ]] && echo "$HOME/.agents/skills" || echo ".agents/skills" ;;
    warp)
      [[ "$scope" == "global" ]] && echo "$HOME/.warp/skills" || echo ".warp/skills" ;;
    trae|trae-ide|bytedance-trae)
      [[ "$scope" == "global" ]] && echo "$HOME/.trae/skills" || echo ".trae/skills" ;;
    pi|pi-agent)
      [[ "$scope" == "global" ]] && echo "$HOME/.pi/agent/skills" || echo ".pi/skills" ;;
    jetbrains|jetbrains-ai|junie)
      [[ "$scope" == "global" ]] && echo "$HOME/.junie/skills" || echo ".junie/skills" ;;
    replit|replit-agent)
      [[ "$scope" == "global" ]] && echo "$HOME/.agents/skills" || echo ".agents/skills" ;;
    factory|droid|factory-droid)
      [[ "$scope" == "global" ]] && echo "$HOME/.factory/skills" || echo ".factory/skills" ;;
    devin|cognition-devin)
      [[ "$scope" == "global" ]] && echo "$HOME/.config/devin/skills" || echo ".agents/skills" ;;
    openhands|all-hands)
      [[ "$scope" == "global" ]] && echo "$HOME/.agents/skills" || echo ".agents/skills" ;;
    goose)
      [[ "$scope" == "global" ]] && echo "$HOME/.agents/skills" || echo ".agents/skills" ;;
    augment)
      [[ "$scope" == "global" ]] && echo "$HOME/.augment/skills" || echo ".augment/skills" ;;
    qwen|qwen-code|alibaba-qwen)
      [[ "$scope" == "global" ]] && echo "$HOME/.qwen/skills" || echo ".qwen/skills" ;;
    *)
      [[ "$scope" == "global" ]] && echo "$HOME/.agents/skills" || echo ".agents/skills" ;;
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
    echo "Available Skills:"
    for i in "${!AVAILABLE[@]}"; do
      printf "  %2d) %s\n" $((i+1)) "${AVAILABLE[$i]}"
    done
    echo ""
    printf "%bEnter Numbers Comma Separated, Or Type all%b\n" "${YELLOW}" "${NC}"
    read -rp "Pick Skills: " PICK || PICK=""
    if [[ "$PICK" == "all" ]]; then
      SKILLS=("${AVAILABLE[@]}")
    else
      IFS=',' read -ra NUMS <<< "$PICK"
      for n in "${NUMS[@]}"; do
        n="${n//[[:space:]]/}"
        [[ "$n" =~ ^[0-9]+$ ]] || continue
        idx=$((n-1))
        if [[ -n "${AVAILABLE[$idx]:-}" ]]; then
          SKILLS+=("${AVAILABLE[$idx]}")
        fi
      done
    fi
  else
    echo "No --skill Or --all Given And No Terminal Attached, So Here Is The Skill List" >&2
    printf "%s\n" "${AVAILABLE[@]}"
    exit 0
  fi
fi

# Same skill typed twice should still install once.
mapfile -t SKILLS < <(printf '%s\n' "${SKILLS[@]}" | awk '!seen[$0]++')

for s in "${SKILLS[@]}"; do
  if ! validateSkillName "$s"; then
    echo "Invalid Skill Name $s" >&2; exit 1
  fi
done

if [[ -n "$CUSTOM_DIR" ]]; then
  if ! isSafePath "$CUSTOM_DIR"; then
    echo "Refusing Unsafe Custom Dir $CUSTOM_DIR" >&2; exit 1
  fi
  DESTS=("$CUSTOM_DIR")
else
  if [[ ${#AGENTS[@]} -eq 0 ]]; then
    if [[ -t 0 && "$SCOPE" == "project" ]]; then
      echo ""
      echo "Where Should The Skills Go? Generic .agents/skills Covers Most Harnesses."
      echo "  1) Generic .agents/skills   - Codex, Antigravity, Amp, Zed, Goose, OpenHands, And Most Others"
      echo "  2) Claude Code              - .claude/skills"
      echo "  3) OpenCode                 - .opencode/skills"
      echo "  4) Antigravity IDE          - ~/.gemini/config/skills When --global"
      echo "  5) Cursor                   - .cursor/skills"
      echo "  6) Windsurf                 - .windsurf/skills"
      echo "  7) GitHub Copilot           - .github/skills"
      echo "  8) Gemini CLI               - .gemini/skills"
      echo "  9) Pick Specific Harnesses"
      read -rp "Pick Destination [1]: " DPICK || DPICK=""
      DPICK=${DPICK:-1}
      case "$DPICK" in
        1) AGENTS=("generic") ;;
        2) AGENTS=("claude-code") ;;
        3) AGENTS=("opencode") ;;
        4) AGENTS=("antigravity") ;;
        5) AGENTS=("cursor") ;;
        6) AGENTS=("windsurf") ;;
        7) AGENTS=("copilot") ;;
        8) AGENTS=("gemini-cli") ;;
        9)
          echo "Supported Harnesses: claude-code, opencode, codex, copilot, gemini-cli, antigravity, cursor, windsurf, cline, kilo-code, roo-code, amp, zed, warp, trae, pi, jetbrains, replit, factory, devin, openhands, goose, augment, qwen, generic"
          read -rp "Enter Harness Names Comma Separated: " APICK || APICK=""
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
    a="${a//[[:space:]]/}"
    a="${a,,}"
    DESTS+=("$(agentToPath "$a" "$SCOPE")")
  done
  # Agents can share one path (codex, zed, goose all read .agents/skills).
  # Dedupe so each destination installs once.
  mapfile -t DESTS < <(printf '%s\n' "${DESTS[@]}" | awk '!seen[$0]++')
fi

printf "\n%bSource%b  %s\n" "${GREEN}" "${NC}" "$SRC"
printf "%bSkills%b  %s\n" "${GREEN}" "${NC}" "${SKILLS[*]}"
printf "%bScope%b   %s\n" "${GREEN}" "${NC}" "$SCOPE"
printf "%bDests%b   %s\n" "${GREEN}" "${NC}" "${DESTS[*]}"
printf "\n"

USE_GH=false
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  if [[ -t 0 ]]; then
    read -rp "Use The gh Skill Installer Where Supported? [y/N]: " GHANS || GHANS=""
    [[ "$GHANS" =~ ^[Yy]$ ]] && USE_GH=true
  fi
fi

for skill in "${SKILLS[@]}"; do
  FOUND=false
  for avail in "${AVAILABLE[@]}"; do
    if [[ "$avail" == "$skill" ]]; then FOUND=true; break; fi
  done
  if [[ "$FOUND" == false ]]; then
    printf "%bSkip Unknown Skill %s%b\n" "${YELLOW}" "$skill" "${NC}"
    continue
  fi
  for dest in "${DESTS[@]}"; do
    TARGET="${dest}/${skill}"
    if [[ "$DRY_RUN" == true ]]; then
      echo "[Dry Run] $skill -> $TARGET"
      continue
    fi
    if [[ "$USE_GH" == true ]]; then
      printf "%bInstalling%b %s Via gh To %s\n" "${GREEN}" "${NC}" "$skill" "$dest"
      if ! gh skill install "${REPO}" "$skill" --agent generic --scope "$SCOPE" --force 2>&1; then
        printf "%bgh Install Failed, Falling Back To Copy%b\n" "${YELLOW}" "${NC}"
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

# Remove the cloned temp repo as soon as copying finishes.
# The EXIT trap is the safety net for early exits and errors.
cleanup

printf "\n%bDone%b. Installed %d Skill(s) To %d Location(s).\n" "${GREEN}" "${NC}" "${#SKILLS[@]}" "${#DESTS[@]}"
if [[ "$SCOPE" == "project" ]]; then
  echo "Project Skills Live In .agents/skills And Are Shared By Most Harnesses."
  echo "Commit Them If You Want Your Team To Get Them Too."
else
  echo "Global Skills Are Now Available In Every Project."
fi
