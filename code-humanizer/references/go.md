# Go

Read this guide for Go code. Follow the module's Go version, package layout,
error conventions, concurrency model, and `go generate` behavior.

## Generated Go Signals

Look for interfaces created before a second implementation exists, constructors
that only assign fields, wrapper types that add no policy, generic `interface{}`
values, ignored errors, unnecessary goroutines, and channels used where a
direct function call is clearer.

Do not delete a single-implementation interface when it is the consumer-owned
test seam or a public package contract.

## Errors

Check errors immediately. Add operation context with `%w` when callers need to
unwrap the cause.

```go
if err := store.Save(ctx, order); err != nil {
    return fmt.Errorf("save order %s: %w", order.ID, err)
}
```

Use `errors.Is` and `errors.As` for classification. Do not compare wrapped
errors by string. Avoid logging and returning the same error at every layer.
Choose one layer to log based on the repository convention.

## Concurrency And Resources

Every goroutine needs an ownership story, a termination path, and cancellation.
Use `context.Context` for request-scoped cancellation. Close response bodies,
stop tickers, and release locks. Do not start a goroutine to make synchronous
work appear sophisticated.

Use `go test -race` for concurrent changes. Check channel closure ownership,
deadlock risks, data races, and duplicate effects on retry.

## APIs And Data

Keep exported names, comments, zero values, and error behavior compatible.
Prefer concrete types at implementation boundaries and small interfaces at
consumer boundaries. Avoid `map[string]any` when a struct expresses the data.
Use JSON tags and validation that match the wire contract.

## Verification

Run `gofmt`, `go vet`, `go test ./...`, and `go test -race ./...` when relevant.
Run `go generate` only when the repository documents it and inspect generated
diffs rather than hand-editing generated output.

## Sources

- https://go.dev/doc/effective_go
- https://go.dev/blog/context
- https://go.dev/doc/diagnostics
