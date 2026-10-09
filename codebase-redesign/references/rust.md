# Rust

## Layout

Single crate:

```
Cargo.toml
src/
  main.rs or lib.rs
  config.rs
  orders.rs        # module root for orders
  orders/
    store.rs
    handlers.rs
tests/             # integration tests, one crate per file
benches/
examples/
```

Workspace with several crates:

```
Cargo.toml         # virtual manifest with [workspace]
crates/
  api/
  core/
  cli/
```

- Cargo discovers `src/main.rs`, `src/lib.rs`, `src/bin/*.rs`, `tests/`, `benches/` and `examples/` on its own. Keep those names.
- A binary that grows logic should move it into `lib.rs` and keep `main.rs` thin. That makes the logic testable from `tests/`.
- Split into a workspace when two binaries share code or compile times hurt. Do not split a small crate.

## Modules

- Rust has two styles for a module with children, `orders.rs` beside an `orders/` folder, or `orders/mod.rs`. The first is the default since the 2018 edition. Use whichever style the repo uses most and apply it everywhere.
- The module tree comes from `mod` declarations, not from folders alone. Moving a file means updating the `mod` line in the parent and every `use crate::...` path.
- Use `pub(crate)` for items the rest of the crate needs and outsiders do not.
- Group modules by domain. Avoid a top-level `utils` module that collects unrelated helpers.

## Naming

- Files, modules and crate names in `snake_case`. Crate names in `Cargo.toml` may use hyphens, and Rust code refers to them with underscores.

## Tests

- Unit tests live in the same file in a `#[cfg(test)] mod tests` block. They move with the file.
- Integration tests go in `tests/` and use only the public API.
- Shared helpers for integration tests go in `tests/common/mod.rs` so Cargo does not treat them as a test crate.

## Moving Files Safely

- rust-analyzer offers code actions to move a module between inline and file forms. For moves across folders, `git mv` and then fix `mod` and `use` lines with the compiler errors as your list.
- Run `cargo check --all-targets` after each batch and `cargo test` at the end.

## Path References to Update

- `mod` declarations and `#[path = "..."]` attributes
- `use crate::` and `use super::` paths
- `include_str!` and `include_bytes!` paths, which are relative to the file
- `build.rs` paths
- `Cargo.toml` `[[bin]]` and `[lib]` `path` entries, `[workspace] members`, and path dependencies between crates
- Re-exports in `lib.rs` that keep a public API stable. Moving a public item in a published crate is a breaking change unless a `pub use` keeps the old path.
