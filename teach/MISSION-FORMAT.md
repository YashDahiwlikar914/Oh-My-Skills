# MISSION.md Format

`MISSION.md` lives at the workspace root. It captures the _reason_ the user is learning this topic. Trace each teaching decision back to this document, including what to teach next, which resources to surface, and which exercises to design.

## Template

```md
# Mission: {Topic}

## Why
{1-3 sentences. The concrete real-world goal the user is chasing. What changes in their life or work when they have this skill? Skip abstract framings like "to understand X" and push for the underlying outcome.}

## Success Looks Like
- {A specific, observable thing the user will be able to do}
- {Another specific thing}
- {…}

## Constraints
- {Time, budget, prior commitments, learning preferences, anything that bounds the approach}

## Out of Scope
- {Adjacent topics the user explicitly does not want to chase right now, protecting the zone of proximal development}
```

## Rules

- **Keep one mission per workspace.** If the user wants to learn two unrelated things, create two workspaces.
- **Prefer concrete over abstract.** "Run a half marathon by October" beats "get fitter." "Ship a Rust CLI to my team" beats "learn Rust."
- **Push back on vagueness.** If the user can't say why they want this, interview them before you write anything. A bad mission is worse than no mission.
- **Revise when reality shifts.** Missions change. When the user's goal moves, update this file so a stale mission doesn't steer future sessions.
- **Keep it short.** A `MISSION.md` that runs past a screen has stopped being a compass and become a plan.
