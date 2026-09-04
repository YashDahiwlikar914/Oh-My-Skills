# Stdlib And Native Alternatives

Use these before adding a dependency. Not exhaustive. Add common ones for the
repo's main language as you find them.

## Python

| Instead of | Use |
|---|---|
| A hand-rolled cache class | `functools.lru_cache` / `cache` |
| Manual dict grouping | `itertools.groupby` (sorted) or `collections.defaultdict` |
| String concat in loop | `"".join(parts)` or f-strings |
| Path string surgery | `pathlib.Path` |
| `while` retry boilerplate | `tenacity`-like loop only if needed; else a bounded `for` |
| Custom enum | `enum.Enum` |
| JSON parse/emit | `json` (stdlib) |
| Dataclass boilerplate | `dataclasses.dataclass` |

## Node / TypeScript

| Instead of | Use |
|---|---|
| Date library (date-fns, dayjs) | `Intl.DateTimeFormat`, `Temporal` if available |
| `lodash` one function | native `Array`/`Object` methods |
| `uuid` package | `crypto.randomUUID()` |
| `clone-deep` | `structuredClone` |
| `node-fetch` | global `fetch` (Node 18+) |
| `fs` callbacks | `fs/promises` |

## Go

| Instead of | Use |
|---|---|
| `github.com/google/uuid` for one id | `crypto/rand` or `math/rand/v2` |
| Third-party set | `map[T]struct{}` |
| `sort` boilerplate | `slices.Sort`, `slices.Contains` |
| Custom sync pool | `sync.Pool` (stdlib) |
| JSON field mapping | `encoding/json` tags |

## Rust

| Instead of | Use |
|---|---|
| `itertools` for simple ops | std `Iterator` methods |
| `lazy_static` | `std::sync::OnceLock` |
| Custom error enum boilerplate | `thiserror` only if project uses it; else `Result<_, Box<dyn Error>>` for small tools |
| `regex` for a fixed prefix | `str::starts_with` |

## Shell

| Instead of | Use |
|---|---|
| A dedicated CLI tool for one transform | `awk`, `sed`, `jq` (if present), parameter expansion |
| `curl` + `jq` parse | `jq` alone when available |
| A loop to find files | `find` / `fd` (if installed) with `-exec` |

## Native platform

- Forms: `<input type="date">`, `<input type="email">`, `<input type="number">` over JS widgets.
- Styling: CSS `gap`, `aspect-ratio`, `clamp()` over JS layout math.
- Data: DB unique/not-null/foreign-key constraints over app-level checks.
- Auth/sessions: framework-provided middleware over a hand-rolled token layer.
