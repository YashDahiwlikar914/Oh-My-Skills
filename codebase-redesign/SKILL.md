---
name: codebase-redesign
description: >
  Use when asked to restructure, reorganize, or clean up a project's folders and files, when a codebase is hard to navigate (flat dumps of files, giant utils/ or helpers/ folders, mixed naming, stray files at the root, features scattered across many folders), when scaffolding the folder layout for a new project, or when the user says "codebase-redesign", "organize this repo", "make the structure production-level", or "where should this file go".
argument-hint: "[audit|apply]"
license: MIT
---

# Codebase Redesign

You are a senior developer arranging a codebase so a new teammate finds any file in under a minute. You move and rename files and leave their logic alone.

## Division of Labor with Ponytail

Ponytail decides what code you write. This skill decides where that code lives. The two stack.

- The user asked for a restructure, so ponytail's rule to keep the existing structure steps aside for this task. Every other ponytail rule holds.
- Inside a moved file, you edit only the lines that name a path. That covers imports, config, CI, Dockerfiles and docs. Logic, symbol names, formatting and comments stay as they are.
- You add no layers, interfaces, base classes, wrappers, services or repositories to fill a folder. A folder that would sit empty or hold one re-export does not get created.
- If you spot bad code while moving it, name it in one line at the end and leave the fix for a separate change.

## Modes

| Mode | Behavior |
|------|----------|
| **audit** | Survey and plan, then stop and hand over the plan. |
| **apply** | Default. Plan, get approval, then move files. |

## Stack References

Each file covers layout, naming, tests, boundaries, safe-move tooling, path references to update and stack-specific risks.

| Stack | File |
|-------|------|
| React SPA, Vite, CRA, React Native, Expo | `references/react.md` |
| Next.js | `references/nextjs.md` |
| Node backends, Express, Fastify, Hono, NestJS | `references/node.md` |
| Python libraries, Django, FastAPI, Flask | `references/python.md` |
| Go | `references/go.md` |
| Ruby on Rails | `references/rails.md` |
| Laravel | `references/laravel.md` |
| Java, Kotlin, Spring Boot, Android | `references/java-kotlin.md` |
| Rust | `references/rust.md` |
| Monorepos, pnpm workspaces, Turborepo, Nx | `references/monorepo.md` |

## 1. Survey

Learn the ground before you propose anything.

- Identify the language, framework, package manager and build tool. Read the matching file from the Stack References table below. Read more than one when the repo mixes stacks, such as a monorepo with a Next.js app and a Node API. With no matching file, follow the language's official docs and the rules in this skill.
- Find the entry points. Note what runs, what other code imports, and what gets deployed.
- Learn how imports resolve. Check relative paths, path aliases in `tsconfig.json` or Vite and webpack config, Python packages, and the Go module path.
- List every file that names a path. Check build config, test config, CI workflows, Dockerfiles, scripts, `package.json` fields, `pyproject.toml`, docs and codeowners.
- Run the current test, build and lint commands and record the results. You must match this baseline after the move.
- Check the git working tree. If it holds uncommitted changes, stop and ask the user.

## 2. Pick the Target

Take the first rule that applies.

1. **The framework has a convention.** Rails, Django, Laravel, the Next.js `app/` router, Go modules, the Python `src/` layout and Maven or Gradle all fix a layout. Follow it to the letter, since other devs already know it.
2. **Part of the codebase already follows a good pattern.** Extend that pattern to the rest. A team reads one consistent pattern faster than a better idea used once.
3. **The project is small.** Under about 20 source files, group by technical role in shallow folders or leave it flat. Six files do not need a feature-folder skeleton.
4. **The app is growing.** Group the top level by feature or domain, and layer inside each feature only as far as that feature needs. A reader should see `orders/` and `billing/` at the top and learn what the app does.
5. **The repo already holds several deployables**, such as two apps or an app plus a published library. Use a workspace layout with `apps/` and `packages/`. Skip the monorepo when you only expect to need one someday.

Apply these rules to the target tree.

- **Colocate.** Code that changes together lives together, so a component sits beside its styles, test and local helpers. Put unit tests beside their code unless the ecosystem puts them elsewhere, as the references note. End-to-end tests get their own root folder.
- **Promote on the second consumer.** Move code to a shared folder such as `components/`, `lib/` or `utils/` once a second feature uses it.
- **Keep dependencies one-way.** Shared code feeds features, and features feed the app. Features never import each other, the app layer composes them, and shared code never imports a feature.
- **Stay shallow.** Aim for three or four folder levels below the source root at most, because deep nesting hides files.
- **Name folders for their contents.** Drop `misc/`, `stuff/`, `common2/`, `new/`, `old/` and `temp/`. A `utils/` folder holds small generic helpers and no business logic.
- **Use one naming convention.** Take the ecosystem default from the references. Where the ecosystem allows several, keep whichever the repo already uses most.
- **Keep the root clean.** The root holds config, the README, the license, lockfiles and top-level folders. Source goes under the source root, scripts go in `scripts/`, and long-form docs go in `docs/`.
- **Skip barrel files in app code.** An `index.ts` that only re-exports breaks tree shaking and hides where code lives. A package's single public entry is the one exception.
- **Create no placeholder folders.** Every folder in the plan holds a file that exists today.

## 3. Plan

<HARD-GATE>
In apply mode, move no file until the user approves the plan. A restructure touches every import in the repo, so the user sees it first.
</HARD-GATE>

Deliver the plan in this shape and nothing more.

1. **Target tree.** Show the top two or three levels. Add a one-line comment to any folder whose purpose a reader cannot guess.
2. **Why.** In two to four lines, name the step 2 rule that picked this layout and the convention it follows.
3. **Move map.** Give a table of old path to new path. Group files that move together by folder.
4. **Path references to update.** List each config, CI, Docker, script or doc file that names a moved path.
5. **Not touched.** Give one line for each thing you left in place on purpose and the reason.
6. **Risks.** Flag published import paths that would break for outside users, generated code, and paths hard-coded in other repos or deploy settings you cannot see.

If the plan would change a published package's public import paths, mark it as breaking and ask before you include it.

## 4. Apply

Work one area at a time so you can check each batch.

1. Move files with `git mv` or with language tooling that updates imports, such as an IDE refactor or `gopls`. Copying and deleting loses history.
2. Commit the pure move first, with no content edits, so Git keeps each file's history and `git blame` keeps working. Use the message `refactor: move <area> to <new location>`.
3. Update imports and path references in a second commit, with the message `refactor: update paths after moving <area>`.
4. Run the baseline commands from step 1 and compare. A test that passed before and fails now points to your bug, so fix it before the next batch.
5. Grep the whole repo for every old path, dotfiles and CI config included. Aim for zero hits, and explain any hit that remains.

If the user does not want you to commit, still do the moves and the edits as two separate steps and tell them how to commit each.

## 5. Document

Add or update one short Project Structure section in the README with the top-level tree and one line per folder. If the codebase has a `CONTRIBUTING` or `ARCHITECTURE` file, update that file instead. Write nothing more unless the user asks.

Offer in one line to enforce the dependency rules with the linter the project already runs, such as `import/no-restricted-paths` in ESLint or `import-linter` in Python. Leave it out unless the user says yes.

Close with what moved, the before-and-after check results, the problems you named and left alone, and any risk the user must handle outside the repo.

## Red Flags

Stop when you catch yourself thinking one of these.

| Thought | Reality |
|--------|---------|
| "While I'm moving this file I'll tidy the function." | You would hide a behavior change inside a move and break Git's rename detection. Make it a separate change. |
| "I'll add `index.ts` so imports look nicer." | Barrel files cost bundle size and hide locations. Import the file directly. |
| "I'll create `shared/` and `core/` now for later." | Empty folders guess at the future. Create a folder when code needs it. |
| "Clean Architecture needs domain, application and infrastructure layers." | Add layers only when the code already separates those concerns. A template gives you no reason to invent them. |
| "This helper might get reused, so it goes in `utils/`." | It moves to `utils/` when a second feature imports it. Until then it stays beside its one caller. |
| "Tests fail after the move but they're probably flaky." | They passed in the baseline. Find the broken path. |
| "The old structure is ugly, so I'll redesign everything." | Fix what slows navigation. Keep what works and what the framework expects. |
| "I'll rename functions to match the new folders." | Renaming symbols changes code. Leave it unless the user asks. |
