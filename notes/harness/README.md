# Harness delivery platform

## Mental model

Harness models software delivery as pipelines composed of stages, steps, services, environments, and infrastructure definitions. Connectors provide access to source, registries, cloud accounts, and clusters. Delegates perform work inside the network boundary and therefore must be treated as privileged agents.

## Pipeline design

Represent build, test, scan, deploy, verification, and rollback as explicit stages. Use templates and reusable steps for consistency, while keeping service-specific choices visible. Parameterize non-secret configuration; store credentials in approved secrets management and grant connectors narrowly. Separate build identity from deployment identity. Make stages observable with clear names, inputs, outputs, and failure messages.

## Governance and safety

Use approvals, policy checks, and environment controls for production changes. Restrict who can edit pipelines, templates, connectors, and secrets. Treat delegate upgrades, network access, and execution isolation as operational responsibilities. Prefer immutable artifacts and deploy by digest/version so verification and rollback refer to a specific build. Test failure paths, not only green runs.

## Operations

Track execution duration, failure rate, queue time, and deployment outcomes. Set reasonable timeouts/retries; retries should not duplicate non-idempotent work. Use verification steps and health signals before declaring success. Document rollback triggers and ownership.

## Practice

Create a pipeline that builds once, scans the artifact, waits for a production approval, deploys the same artifact to staging and production, and automatically halts on failed health verification.

## Further reading

[Harness documentation](https://developer.harness.io/)
