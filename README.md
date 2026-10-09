# Oh My Skills

A collection of agent skills for Claude Code and other coding agents. Each folder holds one skill with a `SKILL.md` file and any references or scripts it loads on demand.

## Install

Clone the repo and copy the skills you want into your Claude Code skills directory.

```bash
git clone https://github.com/YashDahiwlikar914/Oh-My-Skills.git
cp -R Oh-My-Skills/stop-slop ~/.claude/skills/
```

Use `~/.claude/skills/` to make a skill available in every project. Use `.claude/skills/` inside a repo to scope it to that project. Claude Code reads each skill's `description` and loads the full skill when your request matches it. You can also call a skill by name, such as `/stop-slop`.

## Skills

### Planning and Execution

| Skill | Use It When |
|-------|-------------|
| [using-superpowers](using-superpowers) | You start a task and want the agent to pick the right skills first |
| [brainstorming](brainstorming) | You design a feature, explore requirements, or write a spec |
| [writing-plans](writing-plans) | You have a spec and need a step-by-step implementation plan |
| [executing-plans](executing-plans) | You want the current session to work through a plan inline |
| [subagent-driven-development](subagent-driven-development) | You want subagents to implement and review each task in a plan |
| [dispatching-parallel-agents](dispatching-parallel-agents) | You have independent tasks that can run at the same time |
| [handoff](handoff) | You want to end a session and continue in a fresh agent |

### Code Quality

| Skill | Use It When |
|-------|-------------|
| [test-driven-development](test-driven-development) | You write a failing test before any implementation code |
| [systematic-debugging](systematic-debugging) | You hit a bug or failing test and need the root cause before a fix |
| [verification-before-completion](verification-before-completion) | You are about to claim work is done and need evidence first |
| [ponytail](ponytail) | You want the smallest solution and no over-engineering |
| [codebase-redesign](codebase-redesign) | You want to reorganize a project's folders and files |

### Documents

| Skill | Use It When |
|-------|-------------|
| [docx](docx) | You create or edit Word documents |
| [pdf](pdf) | You read, merge, split, fill, or create PDFs |
| [pptx](pptx) | You build or edit slide decks |
| [xlsx](xlsx) | You open, clean, or produce spreadsheets and CSV files |
| [stop-slop](stop-slop) | You draft or edit prose and want to strip AI writing patterns |

### Skills and Learning

| Skill | Use It When |
|-------|-------------|
| [creating-skills](creating-skills) | You create, edit, test, or benchmark a skill |
| [find-skills](find-skills) | You want to discover or install a skill for a task |
| [teach](teach) | You want a guided lesson on a new concept inside your workspace |

## Skill Layout

Every skill follows the same shape.

```
skill-name/
├── SKILL.md       # Frontmatter with name and description, then instructions
├── references/    # Extra docs the agent reads when it needs them
└── scripts/       # Helper scripts the skill runs
```

The `description` field decides when the agent triggers the skill, so write it as a list of concrete situations.

## Credits and Licenses

This repo collects and adapts skills from several sources. Each skill keeps its original license.

- `docx`, `pdf`, `pptx`, and `xlsx` come from Anthropic and carry the proprietary terms in their `LICENSE.txt` files.
- `stop-slop` comes from Hardik Pandya under the MIT License.
- The planning, testing, and debugging skills build on the Superpowers collection by Jesse Vincent.
- `codebase-redesign` and `ponytail` use the MIT License as stated in their frontmatter.

Check a skill's folder before you redistribute it.
