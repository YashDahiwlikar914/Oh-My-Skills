---
name: handoff
description: Use when the user wants to end this session and continue the work in a fresh agent, or asks for a handoff document.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# Handoff

Write a handoff document so a fresh agent can continue this work. The next agent sees only this file, so give it what it needs to act and skip the story of how you got here.

If the user passed arguments, they describe what the next session will focus on. Weight the document toward that work.

## Check the Real State First

Your memory of the conversation can lag behind the files on disk. Confirm the current state with tools before you write. In a git repo, run `git status`, `git branch --show-current` and `git log -1 --oneline`. Record uncommitted changes and failing tests as you observed them.

## Write the Document

Fill this template. Drop any section that would stay empty. Keep the whole document to about one screen, and link to a file whenever a section starts to run long.

```markdown
# Handoff: <short title>

## Goal
<What the user wants, and what done looks like.>

## Current State
<What works, what is half-built, uncommitted changes, failing tests.>

## Next Steps
1. <First concrete action>
2. <Next action>

## Decisions
- <Decision>, because <reason>.

## Dead Ends
- <Approach tried> failed because <reason>.

## Open Questions
- <Choice the user still needs to make.>

## Key Files and Artifacts
- `<path or URL>` holds <purpose>.

## Suggested Skills
- `<skill name>` for <reason>.
```

Follow these rules while filling it in.

- **Record every dead end.** The next agent will retry any approach you leave out.
- **Record the reason behind each decision.** Without it, the next agent will reopen settled questions.
- **Tag unverified claims.** Write "Unverified" next to anything you did not confirm with a tool, so the next agent checks it before building on it.
- **Reference artifacts by path or URL.** Specs, plans, ADRs, issues, commits and diffs already exist. Copying them wastes the next agent's context.
- **Suggest only skills you can see** in your available skills list.
- **Redact secrets.** Remove API keys, passwords, tokens and personal information.

## Save and Report

Save the file to the OS temp directory and keep it out of the workspace. Use `$TMPDIR`, falling back to `/tmp`, or `%TEMP%` on Windows. Name it `Handoff-<YYYYMMDD-HHMM>-<Title-Case-Slug>.md`, for example `Handoff-20261009-1430-Auth-Refactor.md`.

Reply with the full path and a prompt the user can paste into the new session.

```
Read <full path> and continue the work it describes.
```
