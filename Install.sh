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

# curl pipes this script on stdin, so interactive reads must come from /dev/tty.
TTY_FD=""
if { exec {fd}</dev/tty; } 2>/dev/null; then
  TTY_FD="$fd"
fi

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

isSafePath() {
  local p="$1"
  [[ -n "$p" ]] && [[ "$p" != "/" ]] && [[ "$p" != "$HOME" ]]
}

multiSelect() {
  # Checkbox list. Space toggles, arrows or j and k move, a toggles all,
  # enter confirms, q cancels. Selected options land in the outSel array.
  local header="$1"
  local -n inOpts="$2"
  local -n outSel="$3"
  local count=${#inOpts[@]}
  local sel i j key all mark arrow
  outSel=()
  (( count == 0 )) && return 0
  for ((i = 0; i < count; i++)); do sel[i]=0; done
  i=0
  printf "%s\n" "$header"
  printf "\033[?25l"
  while true; do
    printf "\033[%dA" "$count"
    for ((j = 0; j < count; j++)); do
      mark="[ ]"
      arrow=" "
      (( sel[j] == 1 )) && mark="[x]"
      (( j == i )) && arrow=">"
      printf "\033[2K%s %s %s\n" "$arrow" "$mark" "${inOpts[$j]}"
    done
    key=""
    # IFS= matters. read would otherwise strip the space key itself.
    IFS= read -rsn1 -u "$TTY_FD" key || true
    if [[ "$key" == $'\e' ]]; then
      IFS= read -rsn2 -u "$TTY_FD" key || true
      case "$key" in
        '[A') i=$(( (i + count - 1) % count )) ;;
        '[B') i=$(( (i + 1) % count )) ;;
      esac
    elif [[ "$key" == " " ]]; then
      sel[i]=$(( 1 - sel[i] ))
    elif [[ "$key" == "j" ]]; then
      i=$(( (i + 1) % count ))
    elif [[ "$key" == "k" ]]; then
      i=$(( (i + count - 1) % count ))
    elif [[ "$key" == "a" || "$key" == "A" ]]; then
      all=1
      for ((j = 0; j < count; j++)); do (( sel[j] == 1 )) || all=0; done
      for ((j = 0; j < count; j++)); do sel[j]=$(( 1 - all )); done
    elif [[ -z "$key" ]]; then
      for ((j = 0; j < count; j++)); do (( sel[j] == 1 )) && outSel+=("${inOpts[$j]}"); done
      break
    elif [[ "$key" == "q" || "$key" == "Q" ]]; then
      break
    fi
  done
  printf "\033[?25h"
}

agentToPath() {
  # Checked against vendor docs in Sep 2026. The surprises:
  # codex, zed, goose, openhands only read .agents/skills, never their own dir.
  # antigravity reads ~/.gemini/config/skills globally, .agents/skills per project.
  # Echoes "<global>|<project>" and the caller picks a side.
  case "$1" in
    claude-code|claude|anthropic)            echo "$HOME/.claude/skills|.claude/skills" ;;
    opencode)                                echo "$HOME/.config/opencode/skills|.opencode/skills" ;;
    codex|openai-codex|openai)               echo "$HOME/.agents/skills|.agents/skills" ;;
    copilot|github-copilot|github|vscode)    echo "$HOME/.copilot/skills|.github/skills" ;;
    gemini|gemini-cli|google-gemini)         echo "$HOME/.gemini/skills|.gemini/skills" ;;
    antigravity|antigravity-ide|google-antigravity|firebase) echo "$HOME/.gemini/config/skills|.agents/skills" ;;
    cursor|cursor-ide)                       echo "$HOME/.cursor/skills|.cursor/skills" ;;
    windsurf|windsurf-ide|codeium|codeium-windsurf) echo "$HOME/.codeium/windsurf/skills|.windsurf/skills" ;;
    cline)                                   echo "$HOME/.cline/skills|.cline/skills" ;;
    kilo|kilo-code)                          echo "$HOME/.kilo/skills|.kilo/skills" ;;
    roo|roo-code)                            echo "$HOME/.roo/skills|.roo/skills" ;;
    amp|ampcode|sourcegraph-amp)             echo "$HOME/.config/agents/skills|.agents/skills" ;;
    zed)                                     echo "$HOME/.agents/skills|.agents/skills" ;;
    warp)                                    echo "$HOME/.warp/skills|.warp/skills" ;;
    trae|trae-ide|bytedance-trae)            echo "$HOME/.trae/skills|.trae/skills" ;;
    pi|pi-agent)                             echo "$HOME/.pi/agent/skills|.pi/skills" ;;
    jetbrains|jetbrains-ai|junie)            echo "$HOME/.junie/skills|.junie/skills" ;;
    replit|replit-agent)                     echo "$HOME/.agents/skills|.agents/skills" ;;
    factory|droid|factory-droid)             echo "$HOME/.factory/skills|.factory/skills" ;;
    devin|cognition-devin)                   echo "$HOME/.config/devin/skills|.agents/skills" ;;
    openhands|all-hands)                     echo "$HOME/.agents/skills|.agents/skills" ;;
    goose)                                   echo "$HOME/.agents/skills|.agents/skills" ;;
    augment)                                 echo "$HOME/.augment/skills|.augment/skills" ;;
    qwen|qwen-code|alibaba-qwen)             echo "$HOME/.qwen/skills|.qwen/skills" ;;
    *)                                       echo "$HOME/.agents/skills|.agents/skills" ;;
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
  elif [[ -n "$TTY_FD" ]]; then
    multiSelect "Select Skills. Space Toggles, Arrows Or J And K Move, A Selects All, Enter Confirms" AVAILABLE SKILLS
    if [[ ${#SKILLS[@]} -eq 0 ]]; then
      echo "Nothing Selected"
      exit 0
    fi
  else
    echo "No --skill Or --all Given And No Terminal Attached, So Here Is The Skill List" >&2
    printf "%s\n" "${AVAILABLE[@]}"
    exit 0
  fi
fi

# Same skill typed twice should still install once.
mapfile -t SKILLS < <(printf '%s\n' "${SKILLS[@]}" | awk '!seen[$0]++')

# Skill names come from directory names, so they are always this shape.
for s in "${SKILLS[@]}"; do
  if ! [[ "$s" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
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
    if [[ -n "$TTY_FD" ]]; then
      AGENT_CHOICES=(generic claude-code opencode antigravity cursor windsurf copilot codex gemini-cli cline kilo-code roo-code amp zed warp trae pi jetbrains replit factory devin openhands goose augment qwen)
      multiSelect "Select Destinations. Space Toggles, Arrows Or J And K Move, A Selects All, Enter Confirms" AGENT_CHOICES AGENTS
    fi
    if [[ ${#AGENTS[@]} -eq 0 ]]; then
      AGENTS=("generic")
    fi
  fi
  DESTS=()
  for a in "${AGENTS[@]}"; do
    a="${a//[[:space:]]/}"
    a="${a,,}"
    pair="$(agentToPath "$a")"
    if [[ "$SCOPE" == "global" ]]; then
      DESTS+=("${pair%%|*}")
    else
      DESTS+=("${pair##*|}")
    fi
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
if [[ "$DRY_RUN" == false ]] && command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  if [[ -n "$TTY_FD" ]]; then
    IFS= read -ru "$TTY_FD" -rp "Use The gh Skill Installer Where Supported? [y/N]: " GHANS || GHANS=""
    [[ "$GHANS" =~ ^[Yy]$ ]] && USE_GH=true
  fi
fi

for skill in "${SKILLS[@]}"; do
  if ! printf '%s\n' "${AVAILABLE[@]}" | grep -qx -- "$skill"; then
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
      # gh appends the skill name itself, so --dir takes the destination root.
      printf "%bInstalling%b %s Via gh To %s\n" "${GREEN}" "${NC}" "$skill" "$dest"
      if gh skill install "${REPO}" "$skill" --dir "$dest" --force >/dev/null 2>&1; then
        continue
      fi
      printf "%bgh Install Failed, Falling Back To Copy%b\n" "${YELLOW}" "${NC}"
    fi
    printf "%bCopying%b %s -> %s\n" "${GREEN}" "${NC}" "$skill" "$TARGET"
    mkdir -p -- "$TARGET"
    cp -r -- "${SRC}/${skill}/." "$TARGET/"
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
