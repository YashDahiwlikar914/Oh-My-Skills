# The Ladder, Rung By Rung

Ponytail climbs the ladder after it understands the task. Each rung is a
question, not a rule to force. Stop at the first rung that holds.

## Rung 1 — Does this need to exist at all?

Before writing, ask whether the requested thing is solving a real need or a
speculated one.

- Speculative need = skip it, say so in one line. "No config UI needed; env var suffices."
- If the user asked for it explicitly and it has a concrete purpose, keep climbing.

Common miss: a "utility module" created to hold one function, a settings layer
for a value that never varies, a generic repository around one query.

## Rung 2 — Already in this codebase?

Reuse what already lives here. Search before you write.

- Helper, util, type, or pattern a few files over = use it.
- Re-implementing it is the most common slop.
- Match the existing module boundaries and error conventions.

Grep for the operation name, the type, and the likely function. Read the
callers. If a near-equivalent exists, extend it, do not fork it.

## Rung 3 — Stdlib does it?

Use the language standard library before any third-party code.

- Python: `functools.lru_cache`, `itertools`, `pathlib`, `dataclasses`, `enum`.
- Node: `fs/promises`, `crypto`, `URL`, `structuredClone`.
- Go: `net/http`, `encoding/json`, `slices`, `maps`, `sync`.
- Rust: `std::collections`, `std::sync`, `std::fs`, iterators.
- Bash: builtins, `find`, `awk`, `jq` when already present.

See `stdlib-alternatives.md` for concrete replacements.

## Rung 4 — Native platform feature covers it?

Use the platform before a library.

- HTML `<input type="date">` over a date-picker library.
- CSS over JS animations where possible.
- Database constraints (unique, not-null, foreign key) over app-code checks.
- OS or framework primitives over a cross-platform abstraction for one target.

## Rung 5 — Already-installed dependency solves it?

If a dependency the project already uses covers the need, use it. Never add a
new one for what a few lines can do.

- Do not pull a HTTP client library if `fetch` or `requests` is already there.
- Do not add a validation library if the framework's validator is present.

## Rung 6 — Can it be one line?

If the logic is small, write it inline. One clear line beats a named function
with one caller.

- `const displayName = user.name;` not a `buildName`/`getName` pair.
- `sorted(items, key=len)` not a custom comparator class.

## Rung 7 — Only then: the minimum code that works

Write the smallest code that meets the requirement and the guardrails. Cite the
rung you stopped at in your summary.

`[code] → skipped: [X], add when [Y].`
