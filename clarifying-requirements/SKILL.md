---
name: clarifying-requirements
description: Use when a request is vague, underspecified, or has multiple plausible interpretations that could materially change the deliverable, implementation, research scope, design, security action, or file operation. Require only the missing context that affects the result before proceeding. Do not use for simple factual questions, fully specified transformations, or low-risk tasks where assumptions do not change the result.
---

# Clarifying Requirements

## Core Rule

Ask questions before acting when missing information could materially change the result or action. Do not ask for detail merely because a request is short.

The guard applies to the current request and its full conversation context. Do not invent requirements from stereotypes, defaults, or likely intent.

## Activation Test

Activate the clarification gate when at least two plausible interpretations differ in one or more of these areas.

| Area | Examples |
|---|---|
| Outcome | Explanation, implementation, design, report, or recommendation |
| Audience | Personal use, classmates, customers, developers, or executives |
| Scope | One file, one feature, a whole project, or production systems |
| Constraints | Stack, platform, budget, deadline, compatibility, or style |
| Success | Behavior, metrics, acceptance tests, or definition of done |
| Authorization | Ownership, allowed security testing, data access, or deployment rights |
| Side effects | Overwrite, delete, publish, deploy, send, or change live systems |

Do not activate for a simple factual answer, a fully specified transformation, or a reversible low-risk task where a reasonable assumption cannot change the result.

## Gate Procedure

When the gate activates, follow this sequence.

1. Stop before tool use, research, file inspection, implementation, or irreversible reasoning based on an assumption.
2. State what is already understood in one short sentence.
3. Identify the specific missing decisions that could change the result.
4. Ask the smallest sufficient set of relevant questions.
5. Batch independent questions in one message. Ask dependent questions only after their prerequisite answer is known.
6. Ask the questions with the question tool. Give each question constrained choices when they reduce effort. The tool offers a custom answer automatically, so no open choice is needed.
7. Wait for the user response. Do not proceed because the user asks for speed or says to use best judgment.

Ask one to five questions per round when they are independent. Ask fewer when fewer resolve the blockers. Continue in rounds only while material blockers remain.

## Minimum Sufficient Brief

Collect only fields that can change the requested result.

| Task | Ask about when it changes the result |
|---|---|
| Build or modify code | Goal, affected scope, environment, constraints, and acceptance criteria |
| Debugging | Expected behavior, actual behavior, reproduction, environment, and urgency |
| Writing | Purpose, audience, tone, format, length, source material, and exclusions |
| Design | Users, platform, required states, visual direction, and constraints |
| Research | Exact question, scope, time range, location, source standard, and output format |
| Security | Authorization, target, objective, allowed actions, and operational boundaries |
| Files or data | Input, output, schema, validation, overwrite policy, and destination |

Use facts already supplied. Never ask the user to repeat them.

## Exit Conditions

Proceed only when all material blockers are resolved or the user explicitly authorizes assumptions.

Before high-impact, destructive, security-sensitive, or externally visible work, summarize the resolved brief and assumptions, then ask for confirmation if the action could not be safely reversed.

If the user authorizes assumptions for a low-risk task, state the assumptions briefly and proceed. If an assumption could materially increase risk or change the requested outcome, keep asking.

## Question Quality

Ask blockers with the question tool, never as numbered text. Each blocker is one entry in the questions array. The tool adds a type-your-own-answer option automatically.

```text
question: Should it target a static site or a full-stack application?
header: Architecture
options:
  - label: Static site
    description: Fast and simple, no server needed.
  - label: Full-stack application
    description: Backend, database, and user accounts.
```

Call the tool once per round and batch every independent question in that call. Keep headers under 30 characters. Keep option labels under five words and let the description carry the explanation. Set multiple true when more than one option can apply.

Good options expose a decision that changes the output. Options that everyone picks, like yes, no, or I do not know, waste a turn.

Bad questions request a general information dump.

```text
Please provide more details about your project.
```

## Common Rationalizations

| Rationalization | Required response |
|---|---|
| “Just use your best judgment” | Resolve material blockers first. Then state low-risk assumptions. |
| “Inspect the project and figure it out” | Do not inspect first when the missing intent changes what should be inspected or changed. |
| “Use standard defaults” | Defaults are not requirements when different defaults produce different results. |
| “The user needs it quickly” | Ask the smallest blocker set. Speed does not justify hidden assumptions. |
| “I can fix it later” | Do not create avoidable rework when one question can prevent it. |
| “The request is obvious” | Test competing interpretations. Obviousness is not evidence. |

## Red Flags

Stop and reassess when any of these appear.

- You are about to call a tool while a material decision is unresolved.
- You are filling in a stack, audience, scope, or success criterion without evidence.
- You are asking for every possible detail instead of the blocking details.
- You are proceeding because the user expressed urgency.
- You are hiding assumptions inside a plan, command, design, or code change.
- You are treating a security target or permission as implied.

## Examples

### Ask Before Acting

User request

```text
Make me a cybersecurity portfolio website.
```

Response shape

```text
question: Is this a static portfolio or an interactive application?
header: Architecture
options:
  - label: Static portfolio
    description: Plain pages, no server logic.
  - label: Interactive application
    description: Dynamic content or user interaction.

question: Do you have content and projects ready, or should I use placeholders?
header: Content
options:
  - label: Content ready
    description: You provide the projects and copy.
  - label: Use placeholders
    description: I fill the template with examples.
```

### Proceed Without The Gate

User request

```text
Translate “The server is offline” into Hindi.
```

Respond directly because the input, operation, and output language are complete.
