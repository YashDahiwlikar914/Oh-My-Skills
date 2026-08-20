# Rust

Read this guide for Rust code. Check the crate's MSRV, feature flags, unsafe
policy, error type, ownership conventions, and public API stability rules.

This skill prefers camelCase for new local names when the project explicitly
uses that convention. Idiomatic Rust repositories normally require snake_case
through rustfmt and Clippy, so keep snake_case when those tools or the local
crate style require it. Do not rename public API items only for casing.

## API Shape

Prefer predictable APIs over clever generic ones. Keep ownership and borrowing
obvious. Do not add a trait for one private implementation unless it is a real
consumer-owned seam, public extension point, or required by the crate design.

Use the established error crate and conversion style. Avoid `unwrap` and
`expect` on user input, network, file, or configuration paths. Keep them only
when an invariant is proven and the message identifies that invariant.

```rust
let config = loadConfig(path).map_err(|source| ConfigError::Read {
    path: path.to_owned(),
    source,
})?;
```

## Ownership And Async

Do not clone to silence the borrow checker without understanding the cost and
ownership model. Do not add `Arc<Mutex<_>>` as a default escape hatch. Identify
who owns state, who may mutate it, and how locks are ordered.

For async code, keep cancellation, task ownership, backpressure, and shutdown
visible. Do not spawn detached tasks without a join or lifecycle owner.

## Unsafe And Security

Do not remove safety checks, bounds checks, validation, or `unsafe` comments in
the name of simplicity. Every unsafe block needs a local safety argument and a
small scope. Use established cryptographic and serialization crates. Reject
untrusted input before it reaches filesystem, process, network, or deserialization
operations.

## Verification

Run `cargo fmt --check`, `cargo clippy --all-targets --all-features`,
`cargo test`, and `cargo test --release` when release behavior matters. Check
feature combinations and `cargo doc` for public API changes.

## Sources

- https://rust-lang.github.io/api-guidelines/
- https://doc.rust-lang.org/book/
- https://doc.rust-lang.org/nomicon/
