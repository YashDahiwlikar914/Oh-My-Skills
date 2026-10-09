# Next.js App Router

For the Pages Router, the `pages/` folder maps to routes and everything below applies to the code outside it.

## Layout

```
app/                    # routing only, plus route-local code
  (marketing)/          # route group, no URL segment
    page.tsx
    pricing/page.tsx
  (app)/
    layout.tsx
    dashboard/
      page.tsx
      _components/      # private folder, never a route
      actions.ts        # server actions for this route
  api/
    webhooks/route.ts
  layout.tsx
features/               # code shared by several routes in a growing app
  billing/
components/             # UI used across routes
  ui/                   # design system primitives
lib/                    # db client, auth config, fetch helpers
public/                 # stays at the root, even with src/
middleware.ts
```

With `src/`, move `app/`, `features/`, `components/`, `lib/` and `middleware.ts` under it. `public/`, `next.config.*`, `tsconfig.json` and other config stay at the root.

## Rules from the Framework

- A folder becomes a route only once it holds `page` or `route`. You can colocate anything else inside `app/` without it becoming a URL.
- Special file names carry meaning. `layout`, `page`, `loading`, `error`, `not-found`, `template`, `default` and `route` must keep their names and position. Moving one changes routing behavior.
- Prefix a folder with an underscore to keep it out of routing.
- Wrap a folder name in parentheses to group routes and share a layout without changing URLs. Moving a route between groups can change which layout wraps it.
- `@slot` folders hold parallel routes, and `(.)`-style folders hold intercepting routes. Leave both in place unless the user asks to change routing.

## Where Code Goes

- Code used by one route lives in that route's folder, in `_components/` or beside `page.tsx`.
- Code used by two or more routes moves out of `app/` into `components/`, `lib/` or `features/<name>/`.
- Server-only code such as database queries goes in `lib/` or `features/<name>/server/`. Mark it with `import "server-only"` if the project already uses that package.
- Keep `app/` free of deep business logic so a reader can scan it as a sitemap.

## Naming

- Route folders are URL segments, so they use kebab-case, as in `app/order-history/`.
- Other files follow the React conventions in `react.md`.

## Tests

- Unit tests beside the file.
- E2E tests in a root `e2e/` folder.
- Do not put test files inside route folders under names like `page.test.tsx` unless the project already does. Next ignores them, but a reader scanning `app/` as a sitemap trips over them.

## Path References to Update

- `tsconfig.json` `paths`, usually `@/*`
- `next.config.*` settings that name folders, such as `outputFileTracingIncludes`
- `middleware.ts` `matcher`, which lists URLs, so check it when you move routes
- `tailwind.config.*` `content` globs in Tailwind v3
- `components.json` paths if the project uses shadcn/ui
- Hard-coded links and `redirect()` calls if a route URL changes

## Risks

- Moving a route folder changes a public URL. Treat that as a product change and ask first. Moving a folder into or out of a route group leaves URLs alone.
- After a move, run `next build`, which type-checks and catches broken routes. `next dev` alone misses some errors.
