# GitHub Actions for CI/CD

## Mental model

An event starts a workflow; jobs run on hosted or self-hosted runners; steps execute actions or shell commands. Jobs can run in parallel or depend on earlier jobs. Workflows are defined as YAML under `.github/workflows/`, so they are code and require review.

## Workflow design

Use explicit event filters, path/branch conditions where appropriate, job permissions, timeouts, and concurrency groups. Separate validation from deployment. Cache dependencies to improve speed, but never treat a cache as a trusted artifact. Pass data through artifacts with retention appropriate to the use case. Use environments for production approvals and protected environment secrets.

```yaml
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/test.sh
```

Tune `permissions` to the minimum required at workflow/job level. Pin actions to immutable SHAs when policy calls for it. Avoid interpolating untrusted event fields directly into shell commands; pass values through environment variables and validate them. Fork pull requests should not receive secrets. Self-hosted runners need isolation, cleanup, patching, and restricted network access.

## Delivery pattern

Test and scan once, publish an immutable artifact, then promote that artifact through environments. Use OIDC federation for short-lived cloud credentials rather than stored cloud keys. Make deployments idempotent and provide a rollback route.

## Practice

Build a test-and-release pipeline with least-privilege permissions, dependency caching, artifact upload, a protected production environment, and a fork-PR safety check.

## Further reading

[GitHub Actions documentation](https://docs.github.com/actions) · [Security hardening](https://docs.github.com/actions/security-guides/security-hardening-for-github-actions)
