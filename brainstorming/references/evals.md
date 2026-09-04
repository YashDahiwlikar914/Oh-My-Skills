# Brainstorming Skill Evaluations

Use `evaluating-skills` to run these. Capture the current SKILL.md as a baseline
before any edit. Save queries as a single JSON array per file and grade the
candidate against the baseline. Keep held-out prompts the candidate never sees.

## Trigger Evaluation Set

Each block is a valid JSON array: `[{"query": "...", "should_trigger": true}]`.
`run_eval.py` loads the whole file as one JSON value.

### Should trigger (10)

```json
[
  {"query": "Let's build a feature that lets users export their data", "should_trigger": true},
  {"query": "How should we design the auth flow?", "should_trigger": true},
  {"query": "Plan the new billing subsystem", "should_trigger": true},
  {"query": "I have an idea for a CLI tool but not sure how to structure it", "should_trigger": true},
  {"query": "We need to restructure how the API talks to the database", "should_trigger": true},
  {"query": "Design a dashboard for monitoring jobs", "should_trigger": true},
  {"query": "Help me spec out a migration from REST to GraphQL", "should_trigger": true},
  {"query": "What's the best way to add rate limiting to the gateway?", "should_trigger": true},
  {"query": "Brainstorm how to handle offline sync", "should_trigger": true},
  {"query": "I want to add a comments feature to the blog", "should_trigger": true}
]
```

### Indirect and small-task triggers (3)

```json
[
  {"query": "lets make a thing for tracking habits", "should_trigger": true},
  {"query": "can u help me figure out the design for the login page", "should_trigger": true},
  {"query": "just write the code for the parser", "should_trigger": true}
]
```

Note on the last one: the user asks to skip design. The skill should still
trigger (this is an implementation task that needs a design) and then enforce
the gate. The eval measures trigger, not gate compliance — test the gate
separately with the task cases below.

### Should not trigger (10 near misses)

```json
[
  {"query": "Fix the typo in the README", "should_trigger": false},
  {"query": "Why does this test fail?", "should_trigger": false},
  {"query": "Explain what this function does", "should_trigger": false},
  {"query": "Translate this string to French", "should_trigger": false},
  {"query": "Run the linter", "should_trigger": false},
  {"query": "Commit these changes", "should_trigger": false},
  {"query": "What is a monad?", "should_trigger": false},
  {"query": "Update the dependency version", "should_trigger": false},
  {"query": "Delete the temp file", "should_trigger": false},
  {"query": "Show me the git log", "should_trigger": false}
]
```

## Task Performance Cases

Grade these by observable behavior, not just final output.

### Case 1 — Bounded gate holds

**Prompt:** "Add a `--verbose` flag to the existing build script."

**Expect:**
- Classify Bounded
- Explore the script, ask clarifying questions (question tool, constrained choices)
- Present a short design in chat (approach, files, testing)
- STOP and wait for explicit approval before any code
- After approval, implement via TDD, no plan doc

**Fail if:** writes code before approval, or skips the design.

### Case 2 — Architectural handoff

**Prompt:** "Build a plugin system."

**Expect:**
- Classify Architectural
- Write spec from the template, commit it
- Run self-review, dispatch spec reviewer, record Status
- Get user review, then invoke `writing-plans` passing the spec path

**Fail if:** invokes an implementation skill other than `writing-plans`, or
forgets to pass the spec path.

### Case 3 — Anti-pattern resistance

**Prompt:** "Just add the feature, it's simple."

**Expect:**
- Still classify, present a short design (two sentences is fine), and wait for
  approval before implementation

**Fail if:** starts implementing on the "it's simple" framing.

## How To Run

1. Snapshot current `SKILL.md` outside the skill directory (baseline).
2. Save each query block above as `iteration-0/trigger.json` (a single JSON array).
3. Use `evaluating-skills` `scripts/run_eval.py` (Claude-compatible) or the
   runtime-native diagnostic for OpenCode.
4. Grade, save `grading.json` with `text`, `passed`, `evidence`.
5. After edits, re-run on the same set and compare recall, precision, and
   false-trigger rate. Keep at least 3 held-out queries unseen by the revision.
