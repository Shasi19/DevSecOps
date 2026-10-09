# Python scripting for DevOps

## Mental model

Python is useful for APIs, data transformations, automation, and command-line tools. Reliable automation separates argument parsing, domain logic, and side effects. Exceptions and exit codes are part of the interface: callers must be able to distinguish success, invalid input, and operational failure.

## Build maintainable tools

Use `argparse` for CLI options, `pathlib` for paths, `subprocess.run` with argument arrays (not shell strings), and `logging` for diagnostics. Set timeouts on subprocesses and network calls. Check return codes and report actionable errors. Use context managers for files and clients. Type hints, small functions, and tests reduce automation surprises.

```python
import subprocess

result = subprocess.run(
    ["git", "status", "--short"],
    check=True,
    capture_output=True,
    text=True,
    timeout=15,
)
print(result.stdout, end="")
```

Never concatenate untrusted input into a shell command or use `shell=True` without a compelling, reviewed reason. Load secrets from an approved runtime secret source; do not print them or store them in source control. Use virtual environments and pinned dependencies with a lock strategy appropriate to the project.

## Operational behavior

Design retries around idempotency and retryable error classes. Add bounded exponential backoff and jitter for transient remote failures. Make scripts safe to rerun, support dry-run for destructive actions, and emit structured logs/metrics when used in production. Test failure cases such as timeout, permission denial, malformed API data, and partial completion.

## Practice

Write a CLI that checks a service endpoint, validates a response schema, retries transient failures, and returns distinct exit codes. Unit-test the retry policy and test the command against a local mock.

## Further reading

[Python documentation](https://docs.python.org/3/) · [ subprocess](https://docs.python.org/3/library/subprocess.html)
