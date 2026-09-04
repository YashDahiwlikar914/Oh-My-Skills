# Example Brainstorming Sessions

One worked session per path. Use these as the shape of a correct run, not as
strict scripts. The gate and classification rules live in SKILL.md.

## Spike

**Human:** "Can we stream large CSV exports without timing out the request?"

**Agent:** Classifies Spike. Says so aloud.

> This looks like a feasibility question, so I'll treat it as a Spike. I'll
> probe whether our web framework supports streaming responses and whether the
> export job can write incrementally. I'll read the framework docs and one
> similar endpoint, then report back. OK to proceed?

**Human:** "Go ahead."

**Agent:** Investigates cheaply. Reads framework streaming docs, checks one
existing export path.

> Recommendation: Yes. The framework supports chunked streaming. The blocker
> was the export building the whole file in memory. Stream row-by-row to the
> response and the timeout goes away. The throwaway script I wrote proved the
> pattern works on a 2M-row file. Want me to file this as a Bounded task to
> change the real endpoint?

Note: the spike's code stays labeled throwaway. Turning it into real work is a
new classification.

## Bounded

**Human:** "Add a `--json` flag to the existing `report` command."

**Agent:** Classifies Bounded (existing command, small surface). Explores the
command file.

> I found `src/cli/report.py`. It prints a human-readable table. Before I design
> the change, two questions.

Asks via the question tool, one focused round:

- "What should `--json` output cover — the same columns as the table, or a
  richer object?" Options: same columns / richer object.
- "Where should it write — stdout only, or also a file path argument?" Options:
  stdout only / file path flag.

**Human:** "Same columns, stdout only."

**Agent:** Presents short design in chat.

> Design: add `--json` to `report.py`'s argparse. When set, serialize the same
> row tuples currently passed to the table renderer to JSON and print to
> stdout, skipping the table. No change to the table path. Testing: a unit test
> asserts the JSON keys match the column names and that the table path is
> untouched. Files: `src/cli/report.py`, `tests/cli/test_report.py`.

**Agent:** Stops.

> Does this design look right? I won't write code until you say yes.

**Human:** "Yes."

**Agent:** Implements via normal TDD workflow. No spec, no plan doc.

## Architectural

**Human:** "Build a notification system."

**Agent:** Classifies Architectural. Explores. Flags scope first.

> This touches email, in-app, and webhooks. That's three subsystems. I'd
> decompose them and brainstorm the first — say, the delivery core — through the
> normal flow, then spec the others later. Sound right?

**Human:** "Yes, start with delivery core."

**Agent:** Offers the visual companion just-in-time when the dashboard layout
question arises, as its own message. Continues text for the rest.

Asks clarifying questions (purpose, constraints, success criteria). Proposes
2-3 approaches (poller vs webhook receiver vs queue) with a recommendation.
Presents the design in sections, confirming after each.

**Verify step:** Before writing, the agent checks the design against the stated
success criteria (deliver in under 5s, at-least-once, pluggable channels) and
closes a gap where the queue approach didn't cover retries.

**Agent:** Writes the spec from `references/design-doc-template.md`, commits it,
runs the self-review, then dispatches the spec reviewer subagent from
`spec-document-reviewer-prompt.md`. Records Status: Approved.

**Agent:** Asks the user to review the written spec. Waits.

**Human:** "Looks good."

**Agent:** Invokes `writing-plans`, passing the spec path so the plan header's
`Spec:` field is filled:

> Using the writing-plans skill. Spec:
> `.agents/superpowers/specs/2026-08-23-notification-delivery-design.md`.

## Filled Spec Sample (Architectural)

```markdown
# Notification Delivery Core Design

**Status:** Approved
**Date:** 2026-08-23
**Author:** agent + human

## Overview
A channel-agnostic delivery core that sends notifications over pluggable
channels with at-least-once guarantees.

## Goals
- Do: deliver a notification to any registered channel
- Do: survive a channel outage and retry

## Non-Goals
- Don't: build the email/in-app/webhook channel UIs yet
- Don't: user preferences UI

## Requirements
### Functional
- Accept (user_id, channel, payload) and enqueue
- Retry failed deliveries with backoff
### Success Criteria
- Delivery under 5s when channel is healthy
- No silent loss on channel failure
### Constraints
- Must run inside the existing Python service

## Tech Stack
- Python 3.11, existing Redis for the queue

## Global Constraints
- All new code covered by tests (repo rule)
- JSON config only, no YAML

## Architecture
A queue worker pulls jobs and dispatches to a channel adapter. Adapters implement
a single `send(job)` interface.

## Components And Interfaces
| Component | Responsibility | Consumes | Produces |
|---|---|---|---|
| Enqueuer | accepts request, pushes job | API call | queue entry |
| Worker | pulls, dispatches | queue entry | delivery result |
| ChannelAdapter.send(job) | delivers | job | result |

## Data Flow
API -> Enqueuer -> Redis -> Worker -> ChannelAdapter.send -> channel

## Error Handling
Channel timeout -> requeue with backoff, max 5 tries, then dead-letter log.

## Testing Approach
Unit: adapter contract. Integration: worker drains a fake queue. Manual: one real
email in staging.

## Open Questions
- Dead-letter UI deferred to a later spec.

## Out Of Scope
- Channel-specific UIs, user preference store.
```
