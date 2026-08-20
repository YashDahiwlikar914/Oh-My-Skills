# Bash

Read this guide for shell scripts. Bash scripts often look small but run with
high privileges and weak type guarantees. Optimize for explicit failure and
safe quoting, not clever compression.

## Generated Bash Signals

Look for `set -e` used without understanding its exceptions, unquoted
expansions, `eval`, parsing `ls`, temporary files in predictable paths,
subshells that hide status, ignored command failures, repeated flag parsing,
and comments that claim a command is safe without showing why.

Start scripts with the repository's expected shebang. If Bash features are not
needed, use POSIX `sh` only when the project supports it.

Use camelCase for new shell variables and functions when the script's existing
style permits it. Preserve exported environment names, command flags, and
names consumed by other scripts.

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
```

`set -e` is not complete error handling. Inspect commands in conditionals,
pipelines, command substitutions, and subshells. Use explicit checks when a
failure must be handled or reported.

## Quoting And Paths

Quote variable expansions by default. Use arrays for command arguments instead
of building command strings.

```bash
jsonFiles=("$sourceDir"/*.json)
for filePath in "${jsonFiles[@]}"; do
  processFile "$filePath"
done
```

Do not use `eval` to reparse input. Do not pass user input into `sh -c`,
`bash -c`, SQL text, or a command string. Use `--` before paths when the
program supports it. Treat filenames beginning with `-`, spaces, newlines,
globs, and shell metacharacters as normal test cases.

## Temporary Files And Cleanup

Use `mktemp` and a trap for cleanup. Do not create `/tmp/name` directly.
Choose cleanup behavior deliberately when a script receives a signal.

```bash
tmpDir=$(mktemp -d)
cleanup() { rm -rf -- "$tmpDir"; }
trap cleanup EXIT INT TERM
```

Do not use `rm -rf` on a path that could become empty. Validate required
variables before destructive commands and print the resolved target in a dry
run when the operation is high impact.

## Pipelines And Status

Use `pipefail` when pipeline failure matters. Check exit status for commands
whose output drives a decision. Avoid `grep` as a boolean when a clearer test
or the command's own status exists. Do not hide failures with `|| true` unless
the ignored failure is intentional and documented locally.

## Verification

Run `bash -n`, ShellCheck when available, the repository test script, and a
temporary-directory integration test. Test empty input, spaces and newlines in
paths, missing commands, failed network calls, interrupted cleanup, and a dry
run before destructive behavior.

## Sources

- https://www.gnu.org/software/bash/manual/bash.html
- https://www.shellcheck.net/wiki/
- https://mywiki.wooledge.org/BashFAQ/105
