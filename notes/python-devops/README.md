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

[Python documentation](https://docs.python.org/3/) · [subprocess](https://docs.python.org/3/library/subprocess.html)

## Topic roadmap and example

**Core topics:** interpreter/environment, modules and packaging, data structures, exceptions, context managers, iterators, type hints, logging, testing, HTTP/API clients, JSON/YAML parsing, filesystem/process automation, and dependency management. Keep credentials outside config files and avoid logging request headers or payload secrets.

**API automation flow:**

```mermaid
flowchart LR
  CLI[Validate CLI input] --> AUTH[Load scoped identity]
  AUTH --> REQ[Request with timeout]
  REQ --> CHECK[Check status + schema]
  CHECK --> ACTION[Idempotent action]
  ACTION --> LOG[Structured result + exit code]
```

Validate external data at boundaries. Distinguish network timeout, HTTP error, malformed JSON, and schema mismatch. Retry only transient conditions (for example selected 429/5xx responses) with bounded exponential backoff and jitter; respect `Retry-After`. Do not blindly retry non-idempotent operations.

**Troubleshooting:** `ModuleNotFoundError`—confirm interpreter/venv and installed project; subprocess hangs—timeout and capture output carefully; Unicode error—inspect encoding boundary; API 403—identity/scope differs from network failure; duplicate changes—operation lacks idempotency key/state check.

**Revision:** exceptions are control flow only when handled specifically; subprocess argument list avoids shell parsing; timeouts bound work; logs need redaction; a retry policy needs limits and idempotency; unit tests mock boundaries, integration tests verify real contracts.

## Runnable health-check CLI

See [`examples/check_endpoint.py`](examples/check_endpoint.py). It uses only the Python standard library, validates input, bounds request time, distinguishes HTTP/network failures, and returns a nonzero status on failure.

```bash
python3 examples/check_endpoint.py https://example.com/healthz --timeout 3
echo $?
```

Do not use this as a full production SLI probe without reviewing TLS verification, proxy behavior, expected status/body, retry policy, and secret redaction. A single successful request is not a complete availability measurement.

## End-to-end Python automation process

See [`process.md`](process.md) for project/virtualenv setup, CLI/API design, exception and retry policy, tests, packaging, deployment, and secret-safe operations.

## Visual study cards

Browse the [10 original visual study cards](visuals/README.md) as SVG or PNG, covering architecture, workflow, security, delivery, observability, troubleshooting, recovery, resilience, scenarios, and revision.
