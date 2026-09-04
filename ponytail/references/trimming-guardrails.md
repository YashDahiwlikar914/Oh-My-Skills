# Trimming Guardrails (from code-trimming)

These guardrails keep minimal code trustworthy. Apply them as you build with
ponytail, not only at review. For the full review procedure see the
`code-trimming` skill.

## Abstraction test

Keep an abstraction when it owns a real policy, isolates a side effect, protects
a security boundary, provides a public API, creates a useful test seam, or
coordinates a lifecycle or transaction.

Be suspicious of:
- factories with one product
- interfaces with one implementation
- wrappers that only forward calls
- configuration for values that never vary
- generic repositories around one query

Do not remove an abstraction only because it has one implementation. Inspect
callers, tests, public exports, and framework requirements first.

## Boilerplate and symmetry

Remove code that exists only because generated answers often produce complete
structures: unused options, duplicate branches, placeholder callbacks, empty
lifecycle methods, repeated conversions, unreachable fallback cases, parallel
helpers that share no real concept.

Before deleting anything, check for reflection, dynamic imports, plugin
discovery, serialization, code generation, build hooks, migration ordering,
runtime configuration, and external consumers. Search references and inspect
the build system. Do not edit generated or vendored output to make it look
human; change its source or generator instead.

## Names

Use domain names where available. Prefer the shortest name that tells a reader
what the value or operation means in this codebase.

- Replace `data`, `result`, `response`, `item`, `value`, `helper`,
  `processData`, `handleThing`, `utils` when a concrete name exists.
- Keep existing public names, serialized fields, CLI flags, database columns,
  and third-party API names unchanged unless the user requests a breaking
  change.

## Error handling

Trace failures from the boundary to the caller. Remove catch blocks that only
log and continue, generic errors that erase useful context, fallback values
that turn failure into false success, and retries with no bounded reason.

Preserve the local error model. At trust boundaries, validate input, keep
authorization checks, avoid leaking secrets, and make failure behavior
explicit. Do not add broad defensive code for hypothetical failures.

## Tests

Tests describe behavior a caller relies on. Add the smallest test that fails
for the bug or contract at stake. Include boundary cases for authorization,
parsing, state transitions, concurrency, persistence, money, and user-visible
output.

Do not add a large test framework, fixture system, or snapshot suite for one
small function. One runnable assertion beats an empty mock-assertion.

## Local fit

Generated code often imports a library the project avoids, uses a new naming
dialect, chooses a different async or state pattern, or places logic in the
wrong layer. Replace it with the established local approach when that approach
meets the requirement. If the local approach is unsafe or obsolete, make the
reason visible in the diff rather than silently mixing styles.

## Security and reliability

Humanization never lowers a security or reliability guarantee. Treat generated
code as especially suspect around authentication, authorization, input
validation, shell commands, SQL, file paths, deserialization, cryptography,
secrets, network requests, concurrency, and retries.

For these areas, verify the actual contract and test the failure path. Keep
defenses that look repetitive if they protect different boundaries. Do not
replace a safe explicit check with a shorter clever expression without proving
the semantics are unchanged.
