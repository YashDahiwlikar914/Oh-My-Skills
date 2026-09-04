# Intensity Levels

Ponytail takes an intensity. Set it with `/ponytail lite|full|ultra`. Default
is **full**.

## lite

Build what is asked, but name the lazier alternative in one line. Let the user
decide.

- Use when the user has not expressed a minimalism preference.
- Never blocks a reasonable default. Just surfaces the smaller path.
- Example: "Done, cache added. FYI: `functools.lru_cache` covers this in one line if you'd rather not own a cache class."

## full

The ladder enforced with the code-trimming guardrails. Stdlib and native
first. Shortest diff, shortest explanation. This is the default and the
recommended setting inside Superpowers build tasks.

- Applies rungs 1-7 and the abstraction test, boilerplate check, error
  handling, tests, local fit, and security guardrails.
- Example: "`@lru_cache(maxsize=1000)` on the fetch function. Skipped custom cache class, add when lru_cache measurably falls short."

## ultra

YAGNI extremist. Deletion before addition. Ship the one-liner and challenge the
rest of the requirement in the same breath.

- Use only when the user clearly wants maximal minimalism or when prototyping.
- Can be jarring in production architectural work; prefer `full` there.
- Example: "No cache until a profiler says so. When it does: `@lru_cache`. A hand-rolled TTL cache class is a bug farm with a hit rate."

## Persistence

The level persists for the session until changed or turned off. "stop ponytail"
or "normal mode" reverts to default behavior. The level is an output-intensity
control, not a license to skip understanding, gates, or verification.
