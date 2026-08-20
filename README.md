# Oh My Skills

This repo holds my OpenCode agent skills. There are 27 here for development and writing work. Four proprietary format skills are not included because their licenses do not allow public sharing. Those are docx, pdf, pptx, and xlsx.

## Skills

| Skill | Description |
|---|---|
| brainstorming | Turn ideas into designs through collaborative dialogue |
| clarifying-requirements | Ask for missing context before acting |
| code-humanizer | De-AI code and make it maintainable |
| evaluating-skills | Measure skill trigger and task performance |
| executing-plans | Execute a written plan with checkpoints |
| finding-skills | Discover and install skills from the ecosystem |
| finishing-a-branch | Verify and integrate a branch or worktree |
| handoff | Create a compact continuation record for another agent |
| human-writing | Rewrite AI-like prose to sound human |
| omarchy | Customize Omarchy Linux desktop |
| parallel-agents | Dispatch independent tasks concurrently |
| ponytail | Minimal coding solutions, YAGNI approach |
| receiving-code-review | Evaluate and respond to review feedback |
| requesting-code-review | Dispatch an independent reviewer before merge |
| research-paper-writer | Write academic papers in IEEE/ACM style |
| resume-builder | Build resumes via Reactive Resume |
| subagent-development | Execute a plan by dispatching one subagent per task |
| systematic-debugging | Debug failing tests and integration issues |
| teach | Multi-session teaching from foundations to research level |
| test-driven-development | Test-first feature and bugfix workflow |
| using-git-worktrees | Work with isolated git worktrees |
| using-superpowers | Route to the right superpowers skill |
| verification-before-completion | Verify before claiming done or opening a PR |
| web-scraping | Search and extract web content reliably |
| writing-for-agents | Structure agent-facing docs with progressive disclosure |
| writing-plans | Write an implementation plan before coding |
| writing-skills | Author or test a SKILL.md |

## Install

Use the one liner when you want to pick skills. It handles all common harnesses and falls back to a plain copy if you do not have gh.

```bash
curl -fsSL https://raw.githubusercontent.com/YashDahiwlikar914/Oh-My-Skills/main/Install.sh | bash
```

The script shows a numbered list of skills and a list of destinations. Choose the ones you want. It defaults to .agents/skills for the current project. That path works with OpenCode, Cursor, Copilot, Codex, Gemini, Warp, and most others because they check .agents/skills as a fallback.

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

Supported harnesses include opencode, claude-code, cursor, codex, copilot, gemini-cli, cline, windsurf, kilo-code, roo-code, aider, augment, qwen, goose, antigravity, and generic. Generic means .agents/skills. That single path is read by 80 plus harnesses as a fallback. You can also pass any custom path with --dir.
