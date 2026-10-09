# Bash automation script lifecycle

## 1. Specify contract and risk

Write purpose, inputs, outputs, exit codes, side effects, time limit, idempotency, required tools, and secret handling. Classify destructive operations and require explicit confirmation/dry-run. Prefer an existing CLI/API or configuration tool when it is safer than shell automation.

## 2. Implement safely

Use `#!/usr/bin/env bash`, quote expansions, arrays for commands, `set -Eeuo pipefail` with explicit status handling, `printf`, stderr for diagnostics, and `mktemp` plus targeted cleanup trap. Validate all arguments before side effects. Avoid `eval`, parsing `ls`, broad `sudo`, and unbounded globs. Keep secrets out of argv, logs, xtrace, and source.

## 3. Bound external operations

Use timeouts, bounded retries for transient errors only, exponential backoff/jitter, and idempotency. Acquire a lock for shared mutable state. Handle signals and child processes. Write output atomically when partial files would be harmful.

## 4. Test failure modes

Test empty/malformed arguments, spaces/newlines in paths, missing tools, permission errors, timeout, partial failure, interruption, duplicate invocation, and cleanup. Use a temporary directory and mock commands for destructive paths. ShellCheck and a test framework such as Bats can catch common defects.

## 5. Deploy and operate

Version the script; run lint/tests in CI; install with controlled permissions; execute under a dedicated identity and allowlisted environment; log non-sensitive run ID/result/duration. Monitor failures and owner. Never run a newly downloaded script directly in production.

## Incident handling

Stop the specific run safely, preserve logs, identify partial side effects, reconcile state, rotate leaked credentials, and rerun only after idempotency/recovery path is clear.
