# React

Read this guide when the changed code uses React. Follow the version and
rendering model already used by the project. Do not impose a new state or
effect pattern during humanization.

## Component Boundaries

Keep a component when it owns a meaningful UI state, accessibility behavior,
layout boundary, or reusable domain behavior. Inline a wrapper that only
renames props or forwards children when it adds no policy and has no stable
public use.

Prefer names based on user behavior such as `onSearchSubmit` or
`isSaving`, not generic names such as `handleData` or `flag`.

## Hooks

Do not use `useEffect` to derive a value that can be calculated during render.
Do not use an effect to respond to an event that already has an event handler.
Keep effects for synchronizing with an external system.

```tsx
// Unnecessary effect for derived state
const [fullName, setFullName] = useState("");
useEffect(() => setFullName(`${firstName} ${lastName}`), [firstName, lastName]);

// Direct derivation
const fullName = `${firstName} ${lastName}`;
```

Preserve effects that subscribe, connect, disconnect, synchronize a browser
API, or manage an external resource. Check cleanup and dependency behavior.

## Accessibility

Keep labels, roles, keyboard behavior, focus management, live regions, and
semantic elements. Do not replace a native button with a `div` because the
latter looks simpler. Test the behavior that keyboard and assistive technology
users rely on.

## State And Identity

Keep state at the lowest owner that needs it unless the repository uses a state
store. Do not duplicate server state in local state without an invalidation
reason. Do not add `useMemo` or `useCallback` by default. Keep them when they
protect a documented identity contract or avoid measured work.

## Tests

Prefer tests that interact with the rendered UI and assert visible behavior.
Use role and label queries when the project uses Testing Library. Avoid tests
that assert private state, hook call order, or implementation-only markup.
Keep snapshots small and intentional. A snapshot is not a substitute for an
interaction test.

## Verification

Run the repository scripts for lint, typecheck, and tests. For UI changes,
verify loading, empty, error, keyboard, narrow viewport, and normal states when
they are relevant to the component.

## Sources

- https://react.dev/learn/you-might-not-need-an-effect
- https://react.dev/learn/choosing-the-state-structure
- https://react.dev/reference/react/useCallback
- https://testing-library.com/docs/queries/about/
