---
name: brainstorming
description: Use when an idea, feature, component, or change is not yet fully specified and needs design before code. Triggers on requests like "let's build X", "how should we design Y", "plan the feature", or vague implementation asks where intent, requirements, scope, or approach is unsettled. Do not use for clear mechanical processes, one-line fixes, or debugging known failures.
---

# Brainstorming Ideas Into Designs

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by classifying how much process the request needs, then work
through your path: understand the context, refine the idea, present a
design, and get your human partner's approval.

## HARD GATE

Do NOT invoke any implementation skill, write any code, scaffold any
project, or take any implementation action until you have told your
human partner what you intend and they have approved it. This applies
to EVERY task on EVERY path below — the ceremony scales with the task;
the approval gate never does.

## Three Paths

Before your first question, classify the request and say the
classification out loud — "this looks bounded, so I'll present a short
design here rather than write a spec" — so your human partner can
override it:

- **Spike** — a feasibility question ("can we...", "is it possible...",
  "quick and dirty is fine") whose output is an answer, not code you
  keep. Present the question and what you'll try in 2-3 sentences, get
  a nod, then find out as cheaply as correctness allows. No design
  doc, no spec file. Report findings as a recommendation; anything you
  built stays labeled throwaway.
- **Bounded** — a well-scoped change to code that already exists in
  this repo: a new flag, a small endpoint, a one-file fix.
  Understanding the kind of app is not enough — bounded means the flow
  you are changing is already here to read. If there is no existing
  flow to change, the task is not bounded. Ask the clarifying
  questions that matter, present a short design IN CHAT (a few
  sentences to a few short paragraphs), and STOP. Implementation
  starts only after your human partner says yes to that design — a
  bounded task's approval is as hard a gate as an architectural
  one. No spec file, no implementation plan document.
- **Architectural** — new projects, new subsystems, changes that
  restructure how components fit together or alter interfaces others
  depend on. Follow the full process: questions, approaches, sectioned
  design, written spec, then the writing-plans skill.

When in doubt between two paths, take the heavier one. The ratchet is
one-way: hidden complexity discovered mid-task upgrades the path —
stop, say so, and step up. Nothing downgrades mid-task.

## Anti-Pattern: "Too Simple To Need Approval"

Every path ends with your human partner approving your intent before
implementation. A todo list, a single-function utility, a config
change — the design may be two sentences in chat, but you MUST present
it and get approval. "Simple" tasks are where unexamined assumptions
cause the most wasted work. What scales with simplicity is the
artifact, never the approval.

## Red Flags

| Thought | Reality |
|---------|---------|
| "This is too simple to need a design" | Simple means a short design, not no design. Two sentences in chat, then approval. |
| "I'll call it bounded and skip the spec" | Reaching for a label to skip work IS the doubt — take the heavier path. |
| "It's bounded and the design is obvious — I'll start while they read it" | The gate is the approval, not the design's length. Present, then stop until you hear yes. |
| "I understand this kind of app, so it's bounded" | Bounded measures the repo, not your familiarity. A new project has no existing flow — it is architectural. |
| "The spike works, so I'll keep the code" | A spike's output is an answer. Keeping the code is a new request — classify it. |
| "It grew, but I'm almost done — no need to re-classify" | Hidden complexity upgrades the path mid-task. Stop and say so. |
| "They approved the spike, so the follow-up change is approved too" | Each task gets its own classification and its own approval. |

## Asking Questions

Use the **clarifying-requirements** skill to drive your questions. Its
batched, constrained-choice method with the question tool is the
default for gathering the missing decisions that change the design.
When brainstorming needs a single focused question mid-flow, ask one at
a time. Prefer the question tool with options over open-ended text
wherever a decision changes the design.

Before detailed questions, assess scope: if the request describes
multiple independent subsystems (e.g., "build a platform with chat,
file storage, billing, and analytics"), flag this immediately and
decompose before refining details.

## Checklist

Classify first, announce the path, then copy this checklist for your
path and complete items in order.

**Spike:**
- [ ] Explore project context (enough to frame the probe)
- [ ] Present question + probe plan (2-3 sentences)
- [ ] Get approval (a nod is enough)
- [ ] Investigate as cheaply as correctness allows
- [ ] Report findings as a recommendation; label anything built as throwaway

**Bounded:**
- [ ] Explore project context (files, docs, recent commits)
- [ ] Ask clarifying questions (use clarifying-requirements; one at a time when focused)
- [ ] Present short design in chat (approach, files touched, testing)
- [ ] Get approval — STOP and wait for an explicit yes
- [ ] Implement via normal workflow (TDD applies); no plan document

**Architectural:**
- [ ] Explore project context (files, docs, recent commits)
- [ ] Offer the visual companion just-in-time (see Visual Companion)
- [ ] Ask clarifying questions (clarifying-requirements; purpose/constraints/success criteria)
- [ ] Propose 2-3 approaches with trade-offs and your recommendation
- [ ] Present design in sections; get approval after each section
- [ ] Verify against success criteria — before writing, confirm the design meets the stated purpose, constraints, and success criteria; close any gap
- [ ] Write design doc to `.agents/superpowers/specs/YYYY-MM-DD-<topic>-design.md` and commit
- [ ] Spec self-review (placeholder / consistency / scope / ambiguity)
- [ ] Dispatch spec reviewer subagent using `spec-document-reviewer-prompt.md`; record Status
- [ ] User reviews written spec; wait for approval
- [ ] Invoke writing-plans, passing the spec path so it lands in the plan header

## The Design Flow (architectural depth)

Sections below serve bounded and architectural paths (a spike stops at
"present the probe, get a nod"). For the spec skeleton, copy
`references/design-doc-template.md`. For worked examples of each path,
see `references/example-sessions.md`.

**Understanding the idea:** Check project state first (files, docs,
recent commits). For over-scoped requests, decompose into sub-projects
and brainstorm the first through the normal flow. Each sub-project gets
its own spec to plan to implementation cycle.

**Exploring approaches:** Propose 2-3 approaches with trade-offs. Lead
with your recommendation. YAGNI ruthlessly. Apply the `ponytail` ladder
(rungs 1-5: does it exist, need it, reuse, stdlib, native, installed dep)
as the minimal-correct lens when filtering which approaches survive to the
recommendation. Ponytail never writes code before this design's approval gate.

**Presenting the design:** Scale each section to complexity. Ask after
each section whether it looks right. Cover architecture, components,
data flow, error handling, testing.

**Design for isolation:** Break the system into smaller units with one
clear purpose and well-defined interfaces.

**Working in existing codebases:** Follow existing patterns. Include
targeted improvements only where existing code affects the work.

## After The Design (architectural path)

**Documentation:** Write the validated design to
`.agents/superpowers/specs/YYYY-MM-DD-<topic>-design.md`. User preferences
for spec location override this default. Commit the design document to
git.

**Spec Self-Review:** After writing, check with fresh eyes: placeholder
scan, internal consistency, scope, ambiguity. Fix inline.

**Spec Reviewer Dispatch:** Use `spec-document-reviewer-prompt.md` to
dispatch a reviewer subagent. Approve only when Status is Approved or
issues are resolved.

**User Review Gate:** Ask the user to review the written spec before
proceeding. Wait for response. Only proceed once approved.

**Implementation Handoff:** Invoke writing-plans. Pass the spec path
explicitly so the plan header's `Spec:` field is filled. Do NOT invoke
any other skill.

## Visual Companion

A browser-based companion for mockups and diagrams. Available as a tool,
not a mode.

**Offering just-in-time:** Do NOT offer upfront. Wait until a question
would be clearer shown than told. The first time that happens, offer it
as its own message with no other content. Wait for the response. If
accepted, start the server with `--open`. If declined, continue
text-only and don't offer again unless raised.

**Per-question decision:** Even after acceptance, decide for each
question whether to use the browser or terminal. Use the browser for
content that is visual. Use the terminal for text, requirements,
tradeoffs, and scope. See `visual-companion.md` for the full guide and
loop.
