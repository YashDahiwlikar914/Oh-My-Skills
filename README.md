# Oh My Skills

This repo holds my agent skills. There are 34 here for development and writing work. Four format skills are missing, docx, pdf, pptx, and xlsx. Their licenses do not allow public sharing.

## Skills

| Skill | Description |
|---|---|
| brainstorming | Turn ideas into designs through collaborative dialogue |
| clarifying-requirements | Ask for missing context before acting |
| code-humanizer | De-AI code and make it maintainable |
| code-trimming | Review and simplify over-engineered or AI-generated code |
| copywriting | Write conversion-focused marketing copy |
| evaluating-skills | Measure skill trigger and task performance |
| executing-plans | Execute a written plan with checkpoints |
| financial-reasoning | Financial reasoning with Indian context and current data |
| finding-skills | Discover and install skills from the ecosystem |
| finishing-a-branch | Verify and integrate a branch or worktree |
| handoff | Create a compact continuation record for another agent |
| human-writing | Rewrite AI-like prose to sound human |
| legal-writing | Draft and audit legal pages for India-first sites |
| omarchy | Customize Omarchy Linux desktop |
| parallel-agents | Dispatch independent tasks concurrently |
| ponytail | Minimal coding solutions, YAGNI approach |
| prompt-master | Write and improve prompts for AI tools |
| receiving-code-review | Evaluate and respond to review feedback |
| requesting-code-review | Dispatch an independent reviewer before merge |
| research-paper-writer | Write academic papers in IEEE/ACM style |
| resume-builder | Build resumes via Reactive Resume |
| subagent-development | Execute a plan by dispatching one subagent per task |
| systematic-debugging | Debug failing tests and integration issues |
| teach | Multi-session teaching from foundations to research level |
| test-driven-development | Test-first feature and bugfix workflow |
| ui-ux-pro-max | Build and review UI and UX interfaces |
| using-git-worktrees | Work with isolated git worktrees |
| using-superpowers | Route to the right superpowers skill |
| verification-before-completion | Verify before claiming done or opening a PR |
| web-experience-director | Direct web experiences from UI to cinematic 3D |
| web-scraping | Search and extract web content reliably |
| writing-for-agents | Structure agent-facing docs with progressive disclosure |
| writing-plans | Write an implementation plan before coding |
| writing-skills | Author or test a SKILL.md |

## Install

The one liner shows a skill list and a destination list. Toggle what you want with spacebar, move with arrow keys, and confirm with enter. Without gh installed it falls back to a plain copy.

```bash
curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash
```

It defaults to .agents/skills in the current project. OpenCode, Cursor, Copilot, Codex, Gemini, Warp, and most other harnesses read that path as a fallback, so one install covers many tools.

Install every skill without prompting.

```bash
curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --all
```

Install one skill to a specific harness at global scope.

```bash
curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash -s -- --skill parallel-agents --agent claude-code --global
```

List what is available or do a dry run.

```bash
./Install.sh --list
./Install.sh --all --dry-run
```

Use gh when you already have it.

```bash
gh skill install YashDahiwlikar914/Oh-My-Skills --all
gh skill install YashDahiwlikar914/Oh-My-Skills parallel-agents --agent claude-code --scope user
```

Or copy by hand.

```bash
cp -r subagent-development ~/.agents/skills/
cp -r subagent-development ~/.config/opencode/skills/
```

## Harness Paths

I checked every path against the vendor's own docs in September 2026.

| Harness | Global | Project |
|---|---|---|
| claude-code | ~/.claude/skills | .claude/skills |
| opencode | ~/.config/opencode/skills | .opencode/skills |
| codex | ~/.agents/skills | .agents/skills |
| copilot | ~/.copilot/skills | .github/skills |
| gemini-cli | ~/.gemini/skills | .gemini/skills |
| antigravity | ~/.gemini/config/skills | .agents/skills |
| cursor | ~/.cursor/skills | .cursor/skills |
| windsurf | ~/.codeium/windsurf/skills | .windsurf/skills |
| cline | ~/.cline/skills | .cline/skills |
| kilo-code | ~/.kilo/skills | .kilo/skills |
| roo-code | ~/.roo/skills | .roo/skills |
| amp | ~/.config/agents/skills | .agents/skills |
| zed | ~/.agents/skills | .agents/skills |
| warp | ~/.warp/skills | .warp/skills |
| trae | ~/.trae/skills | .trae/skills |
| pi | ~/.pi/agent/skills | .pi/skills |
| jetbrains | ~/.junie/skills | .junie/skills |
| replit | ~/.agents/skills | .agents/skills |
| factory | ~/.factory/skills | .factory/skills |
| devin | ~/.config/devin/skills | .agents/skills |
| openhands | ~/.agents/skills | .agents/skills |
| goose | ~/.agents/skills | .agents/skills |
| augment | ~/.augment/skills | .augment/skills |
| qwen | ~/.qwen/skills | .qwen/skills |

Codex, Zed, Goose, and OpenHands only read .agents/skills. Antigravity reads ~/.gemini/config/skills globally and .agents/skills per project. Generic means .agents/skills, which most harnesses read too. Pass --dir for any custom path. Aider and Continue have no skills support, so they are not listed.
