# General Code Review

Use this guide when the language or framework guide does not cover the change.
Local repository conventions and actual contracts still take priority.

## Human Code Is Evidence Based

Do not add random imperfections, casual names, inconsistent formatting, fake
history, or detector bait. A human maintainer can explain why each important
line exists. Remove code that has no current requirement, no boundary, and no
measurable benefit.

## Abstraction Test

Keep an abstraction when it owns a real policy, isolates a side effect, protects
a security boundary, provides a public API, creates a useful test seam, or
coordinates a lifecycle or transaction. Be suspicious of factories with one
product, interfaces with one implementation, wrappers that only forward calls,
and configuration for values that never vary.

```ts
// Suspicious
const buildName = (user: User) => getName(user);
const getName = (user: User) => user.name;

// Clearer when no policy or boundary exists
const displayName = user.name;
```

Do not remove an abstraction only because it has one implementation. Inspect
callers, tests, public exports, and framework requirements first.

## Comments And Tests

Comments explain why a surprising choice exists, an invariant, or an external
constraint. Delete comments that narrate syntax or repeat a function name.

Tests should fail when the promised behavior breaks. Interaction assertions are
valid when the interaction itself is the contract, such as publishing an event,
writing an audit record, or enqueueing work. They are weak when they replace a
result assertion that the caller actually relies on.

## Special Files

Do not casually rewrite generated output, vendored code, lockfiles, migrations,
schemas, infrastructure configuration, or build hooks. Inspect the generator,
migration runner, package manager, schema consumers, and deployment process.

## Sources

- https://google.github.io/eng-practices/review/reviewer/looking-for.html
- https://martinfowler.com/bliki/Yagni.html
- https://owasp.org/www-project-top-ten/
