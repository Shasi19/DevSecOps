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

## Topic roadmap and delivery flow

**Building blocks:** pipeline contains stages and steps; service describes the application/artifact; environment describes deployment context; infrastructure definition identifies targets; connectors provide source/registry/cloud access; delegates execute tasks in reachable networks. Templates provide reuse but should be versioned and governed.

```mermaid
flowchart LR
  SRC[Source] --> BUILD[Build + test]
  BUILD --> SCAN[Security checks]
  SCAN --> REG[Artifact registry]
  REG --> STAGE[Staging deploy]
  STAGE --> VERIFY[Health verification]
  VERIFY --> GATE[Approval]
  GATE --> PROD[Production deploy]
```

**Example:** build an image once, record its digest and provenance, scan it, deploy that digest to staging, verify metrics/health, then require approval before production. Keep build and deploy connectors distinct and narrowly authorized.

**Troubleshooting:** step cannot reach target—delegate network/DNS/firewall and target endpoint; connector denied—identity, scope, token expiry, and target policy; pipeline hangs—timeouts, delegate capacity, and queue; deploy succeeds but app unhealthy—verify probe semantics and service-specific health, then use the rollback path.

**Revision:** delegate is privileged execution infrastructure; connector grants access; approval does not replace technical verification; retries can duplicate side effects; artifact promotion should preserve immutable identity; template changes can impact many pipelines.

## Production pipeline review checklist

Before enabling a pipeline, document the source branch/event trust level, build identity, artifact repository/digest, delegate network boundary, deployment identity, target scope, approver, verification signal, timeout, retry behavior, rollback action, and audit retention. A branch-controlled pipeline definition is executable code: protect changes to it and its templates.

### Failure scenario: deployment stage reports success but service is unhealthy

Check whether the step's exit status represents only API acceptance or actual workload readiness. Verify deployment status, target health, application error/latency signals, and new revision traffic. If service SLO regresses, halt later stages and use a documented rollback to the exact previous artifact. Do not retry non-idempotent migration/deployment steps automatically.

Review delegate permissions independently from connector permissions. A delegate with broad network reach or a reusable privileged token can exceed the intended scope of a single pipeline.
