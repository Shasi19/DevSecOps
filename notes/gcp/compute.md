# GCP compute: VMs, instance groups, Cloud Run, and GKE

## 1. Choose the least-operational runtime

| Runtime | Good fit | Operational responsibility |
|---|---|---|
| Compute Engine VM | OS/kernel control, legacy or specialized software | Patching, image lifecycle, autoscaling, host hardening |
| Managed instance group | Replicated stateless VM fleet | Instance template, health, rollout and capacity policies |
| Cloud Run | Stateless HTTP/event service or job | Container contract, scaling bounds, concurrency and IAM |
| GKE | Kubernetes API/platform requirements | Workload/platform security, cluster policy, upgrades and capacity |

Do not select Kubernetes by default. Record why a less complex runtime is insufficient.

## 2. Compute Engine production baseline

Use a maintained image family or controlled image pipeline, least-privilege attached service account, no broad project SSH keys, OS Login/IAP-based administration, shielded VM features where appropriate, and private IP unless public access is a requirement. Apply patch policy and inventory. Use startup scripts only for bootstrapping—not as an unversioned configuration-management system.

Use managed instance groups with health checks and rolling updates for replaceable stateless instances. Keep durable state in managed storage/database services. Health checks should detect unusable instances without flapping on transient dependencies.

## 3. Cloud Run baseline

Deploy an immutable image digest; set request/concurrency and min/max instance bounds based on load tests and budget. Choose ingress policy deliberately, use a dedicated runtime service account, and expose only required secrets. Set startup/liveness behavior where appropriate, request timeout, CPU/memory, and VPC egress mode based on actual dependencies.

Example discovery:

```bash
gcloud run services describe SERVICE --region REGION --project PROJECT_ID
gcloud run revisions list --service SERVICE --region REGION --project PROJECT_ID
gcloud run services logs read SERVICE --region REGION --project PROJECT_ID
```

Do not place credentials in environment values checked into source. Verify authenticated and unauthenticated access behavior explicitly.

## 4. GKE platform baseline

If Kubernetes is justified, select Standard vs Autopilot based on node control and operational ownership. Decide regional placement, release channel, authorized control-plane/network access, workload identity, network policy, node/workload isolation, resource requests/limits, Pod security, upgrade windows, and backup/restore. Cluster creation is only the start; bootstrap namespaces/RBAC/policies/observability before workloads.

## 5. Rollout and failure scenario

For a new revision: deploy to a non-production environment; verify health and telemetry; canary or gradually roll out; observe error/latency/saturation; automatically halt on SLO regression; keep a known-good revision available. Rollback is not data rollback—use backward-compatible database migrations.

### Troubleshooting: service returns 5xx after release

Compare revision and traffic split; inspect request logs/traces, startup failures, health checks, dependency latency, quotas, and IAM; check whether a secret/version or schema changed. Roll back traffic to the known-good immutable revision if the release is implicated, then preserve evidence and investigate.

## Revision

VM scaling is not workload correctness; Cloud Run scale-to-zero impacts cold starts; a healthy process may have unhealthy dependency behavior; GKE adds platform operations; immutable digest plus progressive delivery improves rollback confidence.
