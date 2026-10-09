# OCI compute, containers, storage, and databases

## 1. Compute choice

Compute instances offer OS and runtime control with customer patching/hardening duties. OKE provides managed Kubernetes control plane but leaves cluster/workload configuration and lifecycle responsibilities. Container Instances run container workloads without a Kubernetes control plane; verify current feature support, networking, scaling, and operational requirements. Prefer managed/serverless execution only where its constraints meet the service's SLO and network needs.

## 2. Compute production baseline

- Private subnet and no public IP unless there is a documented requirement.
- Bastion or approved identity-aware administration; restrict SSH ingress.
- Current hardened image, patch/maintenance owner, and vulnerability scan.
- Instance/resource principal instead of API keys where supported.
- Boot/block volume encryption, backup policy, monitoring, and deletion protection as appropriate.
- Cloud-init only for safe bootstrap; use a configuration-management or image pipeline for ongoing state.

## 3. Storage semantics

| Service | Use | Operations to decide |
|---|---|---|
| Object Storage | Objects, artifacts, backups, data lakes | Namespace/bucket policy, lifecycle, retention, versioning, replication |
| Block Volume | Attached low-latency block storage | Performance level, backups, attachment mode, encryption, resize |
| File Storage | Shared NFS-style filesystem | Export options, mount targets, subnet/security rules, throughput |

Do not assume object versioning/replication protects from malicious deletion; consider retention controls and isolated backups. Mount-target connectivity is controlled by subnet/NSG/Security List and export options as well as IAM.

## 4. Database selection and recovery

Autonomous Database reduces selected administration; Base Database gives different engine/configuration control. Evaluate engine compatibility, transaction/load profile, latency, HA, patch windows, backup/PITR, network path, encryption, and operational ownership. Replicas support specific read/DR designs but do not replace independent backup and restore testing.

Before migration, benchmark query behavior, test schema compatibility, capture data validation, plan cutover/rollback, and rehearse backup restore. Keep database credentials in Vault; separate database privileges from cloud control-plane permissions.

## 5. OKE workload guardrails

Use dedicated compartments/network boundaries, private API endpoint when supported and operationally suitable, scoped cluster and node identities, workload identity, image scanning, resource requests/limits, Pod security controls, network policies, and controlled upgrade channels. Kubernetes namespace separation alone is not a strong tenant boundary. Plan cluster and node pool upgrades with workload disruption tests.

## Troubleshooting

**Instance is running but application is unavailable:** test health locally, listener address, host firewall, NSG/Security List, route, DNS, load balancer backend health, and app logs. **Block volume not mounted:** inspect attachment state, device discovery, OS partition/filesystem, mount options, and boot persistence; avoid formatting an existing volume. **OKE image pull failure:** verify registry auth, node/workload principal, network/DNS, image path, and architecture.

## Revision

Block and object storage differ; backup and replication differ; compute instance identity is not user API key; OKE managed control plane does not manage your workload reliability; database IAM connection is distinct from SQL authorization.
