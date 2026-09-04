# Python

Read this guide for Python files. Follow the repository's Python version,
formatter, linter, and type checker before applying any example.

The default preference for new names in this skill is camelCase. Python projects
that enforce PEP 8, Ruff naming rules, or an established snake_case style take
precedence. Never rename public Python names, serialized fields, or CLI options
just to change their casing.

## Generated Python Signals

Look for generic `data` and `result` names when domain names exist, one-use
classes, unnecessary `staticmethod` and `classmethod` methods, mutable default
arguments, broad `except Exception`, `assert` used for application validation,
long comprehensions, hidden module state, and decorators that hide I/O.

Use a module-level function instead of a one-method class unless the object owns
state, an interface, a lifecycle, or a test seam.

```python
# Suspicious
class DataProcessor:
    def processData(self, rawData):
        return normalize(rawData)

# Better when no state or boundary exists
def normalizeRecord(recordData):
    return normalize(recordData)
```

## Exceptions

Catch the narrowest expected exception. Keep the `try` block small so a bug in
unrelated code does not get misreported as an expected failure. Re-raise after
adding context when the caller must know the operation failed.

```python
def readConfig(configPath: Path) -> dict[str, object]:
    try:
        return json.loads(configPath.read_text())
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as error:
        raise ConfigError(f"Invalid config at {configPath}") from error
```

Do not catch `BaseException`. Avoid catching `Exception` unless this is a clear
process isolation boundary such as a worker loop. Do not log and return an
empty value when that turns failure into false success.

## Assertions And Types

Use `ValueError`, a project exception, or an explicit result for application
validation. Python may run with assertions disabled.

```python
if limit <= 0:
    raise ValueError("limit must be positive")
```

Add annotations to changed public functions when the project uses them. Do not
invent a large type hierarchy to annotate one local value. Use `None` checks
when `0`, `False`, and empty collections have different meanings.

## Resources And State

Use context managers for files, locks, sockets, and other closeable resources.
Avoid mutable module globals. If a cache or registry is needed, identify its
ownership, lifetime, invalidation, and concurrency behavior.

```python
with path.open("rb") as stream:
    payload = stream.read()
```

## Security

Use parameterized SQL, `subprocess.run` with argument lists and `check=True`,
explicit path policy, bounded timeouts, safe deserializers, and established
cryptographic libraries. Never use `eval`, `exec`, unsafe pickle loading, or
shell interpolation for untrusted input.

Do not include tokens, full request bodies, or sensitive identifiers in logs.
Use `secrets` for security tokens and `hmac.compare_digest` for secret
comparisons where appropriate.

## Verification

Typical checks include `pytest`, `python -m pytest`, `ruff check`, `ruff format
--check`, `mypy`, `pyright`, or the commands defined by `pyproject.toml`.
Verify malformed input, missing files, permission errors, timeout behavior, and
the normal path when the change touches those cases.

## Sources

- https://google.github.io/styleguide/pyguide.html
- https://docs.python.org/3/library/subprocess.html
- https://docs.python.org/3/library/security_warnings.html
