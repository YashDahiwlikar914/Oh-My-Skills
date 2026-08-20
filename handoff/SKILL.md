---
name: handoff
description: Use when ending a session and another agent must continue the work from a compact record of the goal, constraints, verified state, artifacts, blockers, and next action.
---

Create a compact handoff document so another agent can continue without rereading the full conversation. Save it in the operating system's temporary directory, not in the workspace. Do not modify project files, commit changes, or claim work is complete unless the record supports that claim.

## Required Content

Write these sections in this order.

1. `Objective` with the user's requested outcome and explicit acceptance criteria.
2. `Constraints and Decisions` with user preferences, exclusions, chosen approaches, and unresolved questions.
3. `Current State` with `completed`, `in progress`, and `blocked` work. Mark each claim as `verified`, `user stated`, or `unverified` when the distinction matters.
4. `Files and Artifacts` with relevant paths, URLs, branches, commits, and existing plans. Say when a referenced item is missing or was not checked.
5. `Verification` with exact commands run, their result, and known test or build gaps. Do not convert an intended check into a passing result.
6. `Next Action` with the first concrete action the next agent should take, followed by later actions only when they are already known.
7. `Suggested Skills` with only skills that are relevant to the next action. Use the exact skill names available in the current catalog and give one short reason for each.

Preserve exact paths, command names, error messages, and user decisions when they affect continuation. Reference existing specs, plans, ADRs, issues, commits, and diffs instead of copying their contents.

## Fact And Secret Handling

- Separate observed facts from user statements, assumptions, and open questions.
- Never invent a result, file, branch, commit, test, decision, or requirement.
- Remove credentials, API keys, access tokens, cookies, private keys, and raw secrets from copied output. Replace each with `[REDACTED]`.
- Keep only the minimum personal or environment detail needed to continue the work.

## Save And Verify

1. Choose the OS temporary directory. On Unix use `$TMPDIR` when it is set and writable, otherwise `/tmp`. On Windows use `%TEMP%`.
2. Use a unique filename such as `agent-handoff-YYYYMMDD-HHMMSS.md`.
3. Write the document, read it back, and confirm it is non-empty and readable.
4. Check the saved document for secrets and unsupported completion claims before reporting its path.
5. Reply with the exact saved path and a one-sentence status. Do not paste the full document unless the user asks for it.

If the requested focus is narrow, preserve the required sections but keep unrelated sections short. A useful handoff is actionable, not a transcript.
