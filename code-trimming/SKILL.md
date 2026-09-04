---
name: code-trimming
description: Use when reviewing or revising source code, tests, scripts, configuration, types, interfaces, or build and infrastructure definitions that are over-engineered, inconsistent with the repository, difficult to trust or maintain, or AI-generated or heavily AI-edited. Covers executable behavior and structure only. Use human-writing for README, docs, markdown prose, comment wording, docstrings, JSDoc, commit messages, PR descriptions, changelogs, and migration prose.
license: MIT
metadata:
  version: "1.0.0"
---

# Code Humanizer

Improve code until it reads as if its author understood the repository, the
current requirement, and the failure modes. Human code is not code with random
imperfections. It is code with evidence behind its choices.

## Scope

Humanize implementation code, tests, configuration, scripts, types, interfaces,
and build and infrastructure definitions. Do not rewrite behavior merely to
change its visual style. Do not add quirks, typos, fake history, arbitrary
naming, or inconsistent formatting. Do not claim that code is human because a
detector accepts it.

This skill targets executable code and structure. It does not edit natural
language. For README, docs folder files, markdown prose, comment wording,
docstrings, JSDoc, commit messages, PR descriptions, changelogs, or migration
prose, delegate to the human-writing skill. Even when a comment lies about the
code, fix or remove the code it misdescribes rather than polishing the wording.

Treat generated code as untrusted until its assumptions have been checked.
The fact that it compiles is weak evidence. It may still use the wrong local
API, hide an invalid assumption, mishandle a boundary, or add complexity that
the task does not need.

## First Read The Repository

Before editing, inspect enough context to understand the code as a maintainer
would.

1. Read the project README and package or build manifest.
2. Identify the project language, framework, test runner, formatter, linter,
   type checker, and existing test command.
3. Read the complete target file and its direct callers, imports, types, and
   nearby tests.
4. Search for local examples of the same operation before inventing a helper,
   pattern, error type, hook, or abstraction.
5. Check the current diff when the code is part of an ongoing change.
6. Note the project vocabulary, naming, module boundaries, error conventions,
   test style, and level of abstraction.
7. Mark generated files, vendored code, migrations, lockfiles, schemas, and
   deployment configuration before considering edits. Treat them as special
   artifacts, not ordinary source files.

Do not flatten a distinctive local style into a generic style guide. Existing
code is evidence, not absolute authority. Follow it unless it conflicts with
correctness, security, accessibility, or a project rule.

Use camelCase for new local variables, functions, methods, props, and private
members when the project does not impose a stronger naming convention. Keep
PascalCase for types and exported symbols where the language requires it. Keep
existing public names, serialized fields, CLI flags, database columns, and
third-party API names unchanged unless the user requests a breaking change.
Language-specific guides may show a different convention only when a formatter,
linter, compiler rule, or established repository style requires it.

## Decide Whether To Change Anything

Start with the smallest useful question. What makes this code hard to trust,
understand, change, or operate?

Change code when there is a concrete reason such as an unnecessary layer, a
wrong assumption, duplicated policy, unclear ownership, a real edge case, an
unsafe boundary, a misleading name, a misleading comment (verify the code it
describes), or a test that would
not fail for the relevant regression.

Leave code alone when the only complaint is that it looks too polished, uses a
common pattern, has consistent formatting, or could theoretically be written
differently. Humans write clean code. Do not manufacture defects to signal
authorship.

Prefer deletion and local simplification over new structure. Solve the need
that exists now. Add an abstraction when repeated behavior, a public API, a
test seam, a transaction or lifecycle boundary, a security policy, or a stable
domain boundary justifies it. Two callers are useful evidence, not a law.
Future flexibility alone is not a requirement.

## Signals Of Generated Code

These are review prompts, not automatic rewrite rules. Confirm each signal in
the repository before changing it.

### Generic Names

Replace names such as `data`, `result`, `response`, `item`, `value`, `helper`,
`processData`, `handleThing`, and `utils` when a domain name is available. Use
camelCase for the replacement, such as `orderRecords`, `responseBody`, or
`selectedAccount`, unless the local language rules require another form.
Prefer the shortest name that tells a reader what the value or operation means
in this codebase. Do not make names longer just to sound precise.

### Speculative Abstractions

Look for factories with one product, interfaces with one implementation,
configuration for values that never vary, wrappers that only forward calls,
generic repositories around one query, and utility modules created to hold one
function. Inline or delete them when the current requirement does not need the
boundary. Keep an abstraction when it isolates a real side effect, policy,
security boundary, or repeated behavior.

### Boilerplate And Symmetry

Remove code that exists only because generated answers often produce complete
looking structures. Examples include unused options, duplicate branches,
placeholder callbacks, empty lifecycle methods, repeated conversions,
unreachable fallback cases, and parallel helpers that do not share a real
concept. Do not remove validation, cleanup, authorization, retries, or error
handling just because it looks repetitive.

Before deleting anything, check for reflection, dynamic imports, plugin
discovery, serialization, code generation, build hooks, migration ordering,
runtime configuration, and external consumers. Search references and inspect
the build system. Do not edit generated or vendored output to make it look
human. Change its source or generator when that is supported by the project.

### Comments, Docstrings, And Documentation

This skill edits code, not prose. Comment wording, docstrings, JSDoc, README,
docs folder files, changelog entries, and migration prose are natural language
and belong to the human-writing skill. Delegate them there for any wording,
tone, or clarity issue.

When a comment or docstring is wrong about the code, do not rewrite the prose.
Fix the code it misdescribes, or delete the comment when the code is correct.
A misleading comment is a signal to verify the code, not to polish sentences.

### Error Handling

Trace failures from the boundary to the caller. Remove catch blocks that only
log and continue, generic errors that erase useful context, fallback values
that turn failure into false success, and retries with no bounded reason.
Preserve the local error model. At trust boundaries, validate input, keep
authorization checks, avoid leaking secrets, and make failure behavior explicit.

Do not add broad defensive code for hypothetical failures. Handle failures
that the dependency can produce, the interface permits, or the system must
survive. If the code cannot decide safely, fail clearly rather than guessing.

### Tests

Tests should describe behavior a user or caller relies on. Remove tests that
only restate implementation details, assert that a mock was called without
checking the result, duplicate an existing higher-level test, or pass while
the behavior is broken.

Add the smallest test that would fail for the bug or contract at stake. Include
boundary cases when they affect behavior, especially authorization, parsing,
state transitions, concurrency, persistence, money, and user-visible output.
Do not add a large test framework, fixture system, or snapshot suite for one
small function.

### Local Fit

Generated code often imports a library already avoided by the project, uses a
new naming dialect, chooses a different async or state pattern, or places logic
in the wrong layer. Replace it with the established local approach when that
approach meets the requirement. If the local approach is unsafe or clearly
obsolete, make the reason visible in the diff rather than silently mixing
styles.

### Over-Explanation

Reduce ceremony in the code. Do not add a layer or abstraction just to make the
code look considered. A small diff that solves the actual need is better than a
polished structure with no behavioral justification.

## Refactoring Rules

Use this order unless the repository gives a better one.

1. Preserve the public behavior and existing interfaces unless the user asked
   for a breaking change.
2. Remove dead code and unused dependencies.
3. Inline one-use abstractions when no boundary justifies them.
4. Rename unclear local symbols using repository vocabulary.
5. Simplify control flow without hiding important cases.
6. Keep side effects at visible boundaries.
7. Make invalid states and failure paths explicit.
8. Add or repair focused tests.
9. Format only files touched by the task unless the user requested a format
   pass.

Do not perform broad cleanup unrelated to the requested behavior. Large style
diffs hide correctness changes and make review harder.

## Security And Reliability

Humanization never lowers a security or reliability guarantee. Treat generated
code as especially suspect around authentication, authorization, input
validation, shell commands, SQL, file paths, deserialization, cryptography,
secrets, network requests, concurrency, and retries.

For these areas, verify the actual contract and test the failure path. Keep
defenses that look repetitive if they protect different boundaries. Do not
replace a safe explicit check with a shorter clever expression without proving
that the semantics are unchanged.

## Verification

After editing, inspect the diff as a reviewer would. Confirm that every change
has a concrete reason and that the patch still fits the surrounding code.

Run the project-provided formatter, linter, type checker, and relevant tests.
If the project has no automated test command, run the narrowest executable
check available and say what was not verified. Do not report a check as passed
unless it actually ran.

For a non-trivial change, manually verify one normal path and one meaningful
failure or boundary path. For security-sensitive code, verify authorization
and malformed input explicitly. For concurrent code, reason about races and
deadlocks instead of treating a passing unit test as proof of safety.

If no edit is justified, do not run formatters or create a test only to produce
an artifact. Report the files and conventions inspected and the reason for
leaving the code unchanged.

## Boundary Checklist

When code handles external input or privileged effects, inspect the relevant
boundary even if the user only asked for style.

- Authentication and authorization. Check identity, resource ownership, and
  default-deny behavior separately.
- SQL and query builders. Use bound parameters and verify that identifiers,
  sort fields, and filters cannot become raw query text.
- Shell and process execution. Prefer argument arrays, fixed executables,
  bounded timeouts, checked exit status, and explicit environment handling.
- File paths. Establish an allowed root, resolve or reject symlinks as needed,
  prevent traversal, and enforce file type and size limits.
- URLs and network calls. Check schemes, destination policy, redirects,
  timeouts, response limits, and SSRF exposure.
- Deserialization. Use an allowlist of types or a data-only format. Do not
  deserialize attacker-controlled objects merely because a library supports it.
- Secrets and logs. Do not expose tokens, credentials, personal data, or raw
  untrusted strings in logs, errors, snapshots, or test output.
- Cryptography. Use the project's established primitives and libraries. Never
  replace a cryptographic operation with a shorter homemade version.
- Concurrency and retries. Bound attempts, preserve idempotency, and check
  cancellation, locking, ordering, and duplicate effects.

Security checks can look repetitive because separate layers defend separate
assumptions. Remove one only after proving the other layer owns the same
invariant.

## Output

When changing files, make the edits and then report only the useful result.

1. State the concrete code problems found.
2. State the important code changes made.
3. State the verification commands and their results.
4. Mention assumptions or unverified risks.

Do not provide an AI-likeness score. Do not describe code as human because it
contains irregularities. If no change is justified, say so and explain the
evidence briefly. For prose issues found in comments or docs, refer the user to
the human-writing skill rather than editing the wording yourself.

## Evidence Base

This skill applies principles from public engineering guidance rather than
claims that code has a detectable human signature.

- Google Engineering Practices, The Standard of Code Review
  https://google.github.io/eng-practices/review/reviewer/standard.html
- Google Engineering Practices, What to look for in a code review
  https://google.github.io/eng-practices/review/reviewer/looking-for.html
- Martin Fowler, Yagni
  https://martinfowler.com/bliki/Yagni.html
- OWASP Top 10
  https://owasp.org/www-project-top-ten/
- Google Python Style Guide
  https://google.github.io/styleguide/pyguide.html
- Rust API Guidelines
  https://rust-lang.github.io/api-guidelines/

The evidence supports improving code health, reducing unnecessary complexity,
matching local conventions, naming clearly, keeping comments purposeful, and
testing behavior. It does not support changing code to satisfy an AI detector.

For detailed examples, read the matching guide under `references/` when the
task needs language-specific guidance or a second review pass.

- Python files: `references/python.md`
- JavaScript and TypeScript files: `references/javascript-typescript.md`
- React components: `references/react.md`
- Node and Express services: `references/node-express.md`
- Go files: `references/go.md`
- Rust files: `references/rust.md`
- Shell scripts: `references/bash.md`
- Other files or a second review pass: `references/general-review.md`
