# Monorepos

Covers pnpm, npm and Yarn workspaces, Turborepo and Nx.

Adopt this layout once the repo holds two or more deployables or a published library. Turning a single app into a monorepo is a large change of its own. Plan it separately and ask first.

## Layout

```
apps/
  web/
  api/
  docs/
packages/
  ui/               # shared components
  config/           # shared eslint, tsconfig, prettier presets
  db/               # schema, client, migrations
  types/            # only if types are shared and have no better home
package.json        # root scripts and dev tooling only
pnpm-workspace.yaml # or "workspaces" in package.json
turbo.json or nx.json
tsconfig.base.json
```

- Each app inside `apps/` follows its own stack reference, such as `nextjs.md` or `node.md`.
- Each package has its own `package.json`, a name such as `@repo/ui`, and one public entry in `exports`. That entry is the one place a barrel file belongs.

## Boundaries

- Apps never depend on other apps.
- Packages never depend on apps.
- Packages may depend on other packages, without cycles.
- Reference internal packages with `workspace:*` in `package.json`.
- Nx enforces these rules with tags and `@nx/enforce-module-boundaries`. In Turborepo, use the linter rules in `react.md` per app. Offer either and add it only on a yes.

## Shared Config

- Shared tsconfig, ESLint and Prettier presets go in `packages/config/` or one package per tool, and each app extends them.
- Keep the root `package.json` for workspace scripts and dev tooling. Runtime dependencies go in the app or package that uses them.

## Internal Packages

- A package consumed only inside the repo can export TypeScript source directly, with no build step. Turborepo calls these just-in-time packages.
- A published package needs a build step and a versioning tool such as Changesets.
- Do not convert between these styles during a restructure unless the user asks.

## Moving Code into a Package

1. Create the package with its `package.json` and entry.
2. `git mv` the files into it and commit the pure move.
3. Add the package as a `workspace:*` dependency of each consumer.
4. Rewrite imports from relative paths to the package name.
5. Run install, then build and test the whole workspace.

## Path References to Update

- `pnpm-workspace.yaml` or `workspaces` globs
- `turbo.json` task `outputs` and `inputs`, and `nx.json` or `project.json` targets
- `tsconfig.base.json` `paths` and project `references`
- Each app's bundler config if it transpiles internal packages, such as Next.js `transpilePackages`
- CI workflows filtered by folder, such as `paths:` filters in GitHub Actions
- `CODEOWNERS` entries
- Dockerfiles that copy specific workspace folders, or use `turbo prune`
