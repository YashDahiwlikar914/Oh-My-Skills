---
name: writing-plans
description: Use when you have a design spec, architectural document, or clear requirements for a multi-step coding task. Triggers before touching any code to create a structured, step-by-step implementation plan.
---

# Writing Plans

## Overview

Write implementation plans for an engineer who has not seen this codebase or this spec. Assume they write idiomatic code in the project's language once they know the exact interface and the exact test. Assume they make a reasonable choice wherever the plan leaves one open. They cannot know what you decided, so write it down. Name the files, the names and signatures, the values from the spec, and the tests that prove each task. Give them the whole plan as bite-sized tasks. Follow DRY, YAGNI, and TDD, and commit often.

**Context.** If the work happens in an isolated worktree, someone should have created it before execution starts.

**Save Plans To** `.agents/Plans/YYYY-MM-DD-<Feature-Name>-Plan.md` in the working directory, next to the spec in `.agents/Specs/`.
- Create the folder if it does not exist. Write the feature name in Title Case with hyphens between words, such as `2026-10-08-Login-Flow-Plan.md`.
- Your human partner's stated plan location overrides this default.
- Do not commit the plan. Your human partner decides what goes into git.

## Scope Check

A spec that covers several independent subsystems should have become separate sub-project specs during brainstorming. If it did not, suggest one plan per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before you define tasks, list the files you will create or modify and what each one does. You lock in decomposition decisions here.

- Design units with clear boundaries and well-defined interfaces. Give each file one responsibility.
- You reason best about code that fits in your context, and your edits hold up better in focused files. Prefer small, focused files over large ones that do too much.
- Keep files that change together in one place. Split by responsibility and leave technical layers out of the split.
- In existing codebases, follow established patterns. If the codebase uses large files, leave the structure alone. If a file you modify has grown unwieldy, you may include a split in the plan.

This structure drives the task breakdown. Each task should produce a self-contained change that makes sense on its own.

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and deserves a
fresh reviewer's gate. Fold setup, configuration, scaffolding, and
documentation steps into the task whose deliverable needs them. Split a
task only where a reviewer could reject one half while approving the
other. Each task ends with a deliverable you can test on its own.

## Step Granularity

**Each step is one action with a result you can check.**
- "Write the failing test" is a step.
- "Run it to make sure it fails" is a step.
- "Implement the minimal code to make the test pass" is a step.
- "Run the tests and make sure they pass" is a step.
- "Commit" is a step.

## Plan Document Header

**Start every plan with this header.**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [Two or three sentences about the approach]

**Tech Stack:** [Key technologies and libraries]

**Spec:** [Path to the spec this plan implements. The plan argues from the
spec, so the spec travels with it. Executors read both.]

## Global Constraints

[The spec's project-wide requirements, such as version floors, dependency
limits, naming and copy rules, and platform requirements. Write one line
each and copy the exact values from the spec. Every task's requirements
include this section.]

## Review Focus

[The five input classes or failure modes that the spec implies, that no
task's tests exercise, and that would hurt a person using this software
most. Write one line each. Name the input or condition and the behavior a
reasonable person would expect, most likely first. The spec describes a
vision. It says what the software must do and leaves out much of what the
software will meet. Its silence on an input gives that input no permission
to break the program. Write this list once, with the spec in front of you.
Then add the test for each line to the task that owns the code, in that
task's step style.]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [What this task uses from earlier tasks, with exact signatures]
- Produces: [What later tasks rely on, with exact function names, parameter
  types, and return types. An implementer sees only their own task. This
  block tells them the names and types that neighboring tasks use.]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Implement `function(input: InputType) -> ResultType` in `exact/path/to/file.py`**

Add one line on the approach when the signature and the test leave a
choice, such as which library call or which data structure. Add a code
block only for an algorithm they do not determine.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## What A Step Contains

A step is done when the implementer can write one reasonable thing from
it. The step must be unambiguous. It does not need to be complete. Each
kind of step carries what makes it unambiguous and nothing more.

- **A test step** gives the test's name and its assertions as code, with
  the spec's exact values in them.
- **A code step** gives the exact signature with its name, parameters, and
  return type. It also gives the file and the values the spec pins. The
  implementer writes the body. Include a body only for an algorithm the
  signature and tests leave open, or for exact copy the spec fixes.
- **A verification step** gives the command to run and the output that
  means it passed.
- **A reference to another task** points to that task's Interfaces block.
  The plan does not repeat that task's code.

A plan holds the decisions the implementer cannot make alone. A plan
longer than the code it describes has written the code instead. Lines
that decide nothing fail the other way. Examples include "TBD", "handle
edge cases", "add appropriate validation", "write tests for the above",
and a type or function that no task defines. The self-review catches both
failures.

## Self-Review

After you write the whole plan, reread the spec and check the plan against it. You run this checklist yourself. Do not dispatch a subagent for it.

**1. Spec Coverage.** Skim each section and requirement in the spec. Point to the task that implements each one and list any gaps.

**2. Step Scan.** Each step must let the implementer write one reasonable thing and carry no more than that. A line that decides nothing is a gap. A function body that the signature and tests already determine is a transcript. Fix both.

**3. Type Consistency.** Check that the types, method signatures, and property names in later tasks match the ones you defined in earlier tasks. A function called `clearLayers()` in Task 3 and `clearFullLayers()` in Task 7 is a bug.

**4. Review Focus.** For each input class or failure mode the spec implies, find a task whose tests exercise it. Put the five uncovered ones most likely to hurt a person in the Review Focus section, and add the test for each line to the task that owns it. An empty section means you checked and found none. It never means you skipped the check.

**5. Proportion.** Compare the plan's length to the spec's. A plan several times longer than its spec transcribes the program. If code blocks fill most of the document, replace bodies with signatures, test names, and assertions. Then check that each step stays unambiguous.

Fix issues inline and move on without a second review pass. If you find a spec requirement with no task, add the task.

## Execution Handoff

After you save and self-review the plan, link it for your human partner
to read. If they already named an execution method, ask them to review
the plan and confirm it captures what they want. Wait for that review
before implementation, then use the method they named. Otherwise, ask them
to review the plan and choose an execution method before implementation.

**When Your Partner Has Not Named An Execution Method**

**"The plan is saved to `.agents/Plans/<filename>.md`. Please review it. Which execution approach do you want?**

- **Subagent-driven.** A fresh subagent implements each task, and a fresh reviewer checks it before the next one starts. A whole-branch review runs at the end. This option is the most thorough and costs a fresh context per task and per review.
- **Native.** I implement each task myself in this session the way this harness runs work. One fresh reviewer on the most capable model then checks the whole branch. This option is the cheapest and fastest, with no independent review until the end. It runs well on a mid-tier session model because the plan carries the design.

**For this plan I recommend <one of the two>, because <one sentence from the plan about how much the tasks depend on each other's interfaces, how many there are, and what a shipped mistake would cost>. Does the plan capture what you want, and which approach should we use?"**

**When Your Partner Has Named An Execution Method**

**"The plan is saved to `.agents/Plans/<filename>.md`. Please review it. Does it capture what you want?"**

**If Your Partner Chooses Subagent-Driven**
- **REQUIRED SUB-SKILL.** Use superpowers:subagent-driven-development

**If Your Partner Chooses Native**
- **REQUIRED SUB-SKILL.** Use superpowers:executing-plans
