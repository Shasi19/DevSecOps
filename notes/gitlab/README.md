# GitLab for DevOps

## Mental model

GitLab combines source management, merge requests, CI/CD, registries, security features, and project planning. A `.gitlab-ci.yml` file describes pipelines as stages and jobs; runners execute jobs using shell, Docker, Kubernetes, or other executors. Runner configuration defines an important trust boundary.

## Pipeline workflow

Start with deterministic stages such as validate, test, package, scan, and deploy. Use `rules` to express when jobs run; avoid brittle combinations of legacy-only/except logic. Cache reusable dependencies, but publish build outputs as artifacts. Make dependencies between jobs explicit with `needs` where it improves graph execution. Scope artifacts and retain them only as long as needed.

## Security and release controls

Protect branches, tags, environments, and CI variables. Masking is not a substitute for restricting who can run jobs or view logs. Never expose secrets to untrusted merge-request code. Use isolated, ephemeral runners for untrusted workloads; privileged Docker-in-Docker and persistent runners need extra scrutiny. Prefer short-lived OIDC-based cloud identity when supported. Scan dependencies, containers, and IaC, and make findings actionable through policy.

## Operations

Monitor runner capacity and queue time, and keep runners patched. Keep deployment credentials separate from build credentials. Promote immutable artifacts rather than rebuilding independently for production. Define manual approvals and rollback behavior for production.

## Practice

Build a pipeline that tests a merge request, produces one image digest, scans it, and deploys that exact digest to a staging environment. Verify an untrusted fork cannot access protected variables.

## Further reading

[GitLab CI/CD documentation](https://docs.gitlab.com/ci/) · [Pipeline security](https://docs.gitlab.com/ci/pipeline_security/)
