# JavaScript And TypeScript

Read this guide for `.js`, `.jsx`, `.ts`, and `.tsx` code. Check the repository
for its runtime, module system, compiler settings, and package scripts first.

## Generated Code Signals

Look for `utils` modules with unrelated functions, `data` and `result` values,
unnecessary `useCallback` or `useMemo`, wrappers around one expression,
duplicated runtime validation, `any` added to silence the compiler, assertions
that only inspect mocks, and promise chains that hide failure behavior.

Do not remove a memoization hook without checking whether a memoized child or
effect depends on identity. Do not add memoization because it appears in an AI
template.

```ts
// Usually unnecessary for a local handler with no identity consumer
const onChange = useCallback(
  (event: ChangeEvent<HTMLInputElement>) => setQuery(event.target.value),
  [],
);

// Direct and readable when the identity is not part of the contract
const onChange = (event: ChangeEvent<HTMLInputElement>) => {
  setQuery(event.target.value);
};
```

## Type Design

Use the project's existing domain types and discriminated unions. Prefer a
small accurate type to a generic `Record<string, unknown>` or `any`. Do not
turn every internal object into a public interface. Keep runtime validation at
boundaries because TypeScript types disappear at runtime.

```ts
type ParseResult =
  | { ok: true; value: Config }
  | { ok: false; error: ConfigError };
```

Do not use non-null assertions or broad casts to silence a real uncertainty.
Trace the source of the value and handle the missing case.

## Async And Errors

Await promises whose failure matters. Preserve rejection context. Avoid
`catch` blocks that log and return `undefined`, and avoid `Promise.all` when one
failure must not cancel or hide the status of other operations.

```ts
try {
  return await client.fetchUser(userId);
} catch (error) {
  throw new UserLookupError(userId, { cause: error });
}
```

Use the repository's error classes and logging policy. Do not put secrets or
raw untrusted payloads in error messages.

## Browser And Node Boundaries

Validate URL schemes, response status, response size, redirects, and timeout
behavior for network calls. Use `node:fs/promises` with explicit paths and
`node:child_process` with argument arrays. Never build SQL, shell commands, or
HTML by concatenating untrusted strings.

Use `textContent` or framework escaping for user content. Preserve CSRF,
authorization, cookie, and security-header behavior while simplifying UI code.

## Tests And Tooling

Test visible behavior, serialized output, error behavior, and accessibility
where they are part of the contract. Keep interaction assertions for real side
effects such as event publication or queueing. Do not use snapshots as proof
that business behavior is correct.

Run the scripts from `package.json`. Common checks include `npm test`, `npm run
lint`, `npm run typecheck`, `tsc --noEmit`, and the repository formatter.

## Sources

- https://www.typescriptlang.org/docs/handbook/2/everyday-types.html
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function
- https://nodejs.org/api/child_process.html
- https://nodejs.org/api/fs.html
