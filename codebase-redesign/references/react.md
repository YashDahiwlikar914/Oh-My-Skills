# React SPA and React Native

Covers Vite, CRA and React Native apps. For Next.js, read `nextjs.md`. The layout follows bulletproof-react.

## Layout

Small app, under about 20 components:

```
src/
  components/
  hooks/
  lib/
  App.tsx
  main.tsx
```

Growing app:

```
src/
  app/            # routes, root component, providers, router
    routes/
  features/       # most code lives here
    auth/
      api/        # requests and query hooks for this feature
      components/
      hooks/
      stores/
      types/
      utils/
    billing/
  components/     # UI used by 2+ features
  hooks/          # hooks used by 2+ features
  lib/            # preconfigured libraries: api client, query client, i18n
  stores/         # global state
  config/         # env vars and app-wide constants
  types/          # types shared across features
  utils/          # small generic helpers
  testing/        # test setup, mocks, render helpers
  assets/
```

A feature gets only the subfolders it needs. A feature with three files keeps them flat inside `features/<name>/`.

## Boundaries

- Imports flow from shared folders to `features/` to `app/`. Shared folders never import a feature, and features never import `app/`.
- Features never import each other. When two features need to work together, the route or page in `app/` composes them.
- A feature that needs another feature's types or API call is a sign the code belongs in a shared folder. Move it there once the second feature uses it.
- Enforce the rules with `import/no-restricted-paths` from `eslint-plugin-import`, one zone per feature. Offer this and add it only on a yes.

## Naming

- Files and folders in kebab-case by default, as in `user-avatar.tsx`. If most component files in the repo use PascalCase, keep PascalCase.
- Hooks start with `use`, as in `use-auth.ts` or `useAuth.ts`, matching the file naming above.
- One component per file for exported components. Small private subcomponents can stay in the same file.
- `eslint-plugin-check-file` can enforce file name casing.

## Tests

- Unit and component tests sit beside the file, as in `user-avatar.test.tsx`.
- Shared test setup goes in `src/testing/`.
- E2E tests with Playwright or Cypress go in a root `e2e/` folder. They test flows and should survive any move inside `src/`.
- Storybook stories sit beside the component, as in `user-avatar.stories.tsx`.

## Barrel Files

Skip `index.ts` files that only re-export. They break tree shaking in Vite, slow dev servers and tests, and create circular imports. Import the file directly, as in `@/features/auth/components/login-form`.

## Moving Files Safely

- VS Code and WebStorm update TypeScript imports when you move a file inside the editor. From the terminal, `git mv` the files and then fix imports with the compiler's errors as your list.
- `tsc --noEmit` catches every broken import in a TypeScript project. Run it after each batch.
- `knip` finds files nothing imports. Run it before planning, since dead files should go on the "named, not fixed" list.

## Path References to Update

- `tsconfig.json` `paths` and `baseUrl`
- `vite.config.ts` `resolve.alias`
- Jest `moduleNameMapper` or Vitest `alias` and `setupFiles`
- `.storybook/main.ts` `stories` globs
- `tailwind.config.js` `content` globs in Tailwind v3
- ESLint config overrides that target folders
- Lazy routes with `import()` strings, which the compiler checks, and `require.context` or `import.meta.glob` patterns, which it does not

## React Native Notes

- Keep `android/`, `ios/`, `app.json` and `index.js` at the root. Native build files reference them.
- Expo Router uses `app/` for routes like Next.js. Put feature code outside it.
- `babel-plugin-module-resolver` aliases in `babel.config.js` need the same updates as `tsconfig.json`.
- Metro caches paths. Run `npx react-native start --reset-cache` or `npx expo start -c` after a move.
