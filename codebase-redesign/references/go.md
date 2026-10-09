# Go

The official guide lives at go.dev/doc/modules/layout. The core Go team never endorsed `golang-standards/project-layout`. Do not copy it wholesale, and do not add `pkg/` because that repo has one.

## Layout

Single binary, small:

```
go.mod
main.go
store.go
handler.go
```

Single binary, growing:

```
go.mod
main.go
internal/
  orders/
  billing/
  platform/      # db, logging, http server setup
```

Several binaries:

```
go.mod
cmd/
  api/main.go
  worker/main.go
internal/
  orders/
  billing/
  platform/
```

Library with a command:

```
go.mod
mylib.go          # importable package at the root
cmd/mytool/main.go
internal/
```

- Put code in `internal/` unless outside modules must import it. The compiler blocks outside imports of `internal/`, so you can move things later without breaking anyone.
- `main` packages stay thin. They parse config, wire dependencies and call into `internal/`.

## Packages

- Name a package for what it provides, in one short lowercase word with no underscores or mixedCaps, such as `orders`, `auth`, `postgres`.
- Avoid `util`, `utils`, `common`, `helpers`, `models`, `types` and `base` packages. Put each function in the package that uses it or in a package named for its purpose.
- The folder name and the package name match.
- Group by domain, not by layer. Avoid top-level `controllers/`, `services/` and `repositories/` packages.

## Import Cycles

Go forbids import cycles. Grouping by domain often creates one when `orders` needs `users` and `users` needs `orders`. Fix it by:

1. Moving the shared types into the package that owns them and having the other one depend on it one way.
2. Defining a small interface in the consumer package.
3. Moving the shared piece into a lower package both import.

Plan the dependency direction before moving files. A plan that creates a cycle does not compile.

## Tests

- `_test.go` files sit beside the code. No separate test tree.
- Test data goes in a `testdata/` folder, which the Go tool ignores.
- Black-box tests use `package orders_test` in the same folder.

## Moving Files Safely

- Moving a package changes its import path. `git mv` the folder, then update the import paths across the module and run `goimports -w .` to fix grouping.
- `gopls` renames identifiers and updates every reference. Use it only if the user asked for symbol renames.
- After each batch, run `go build ./...`, `go vet ./...` and `go test ./...`.

## Path References to Update

- Every import path that contains the old package path
- `go:embed` patterns, which use paths relative to the package folder
- `go:generate` lines with relative paths
- `Makefile` and `Dockerfile` `go build ./cmd/...` targets
- `.goreleaser.yaml` `main` entries
- CI workflows that build specific packages

## Risks

- Moving a non-internal package breaks every outside module that imports it. Treat it as a breaking change and ask first.
- Changing the module path in `go.mod` breaks all importers. Leave it alone unless the user asks.
