# Compute Engine VM: purpose, creation, use, and cleanup

## What a VM is for

Compute Engine VMs suit software requiring an OS, custom kernel/agent, legacy runtime, specialized CPU/GPU/memory, or direct host administration. Prefer Cloud Run, Functions, or managed services when OS control is unnecessary. A single VM is a failure domain; use a managed instance group across zones for replaceable stateless production capacity.

## Before creating the instance

Use a sandbox project with billing, API, quota, budget alert, and owner. Select a Region/zone, private subnet, no external IP, approved image/machine type, dedicated service account, and management method (IAP/OS Login). Ensure VPC firewall allows SSH only from the IAP TCP forwarding range to the intended target, not from all Internet. Plan patching, monitoring, disk backup, and teardown.

## Create a private VM (instructional `gcloud`)

This assumes the VPC/subnet and firewall path are already configured. A service account and `cloud-platform` OAuth scope do not grant broad IAM by themselves; IAM roles on that service account must still be narrowly scoped.

```bash
export PROJECT_ID=REPLACE_SANDBOX_PROJECT
export REGION=us-central1
export ZONE=us-central1-a
export SUBNET=REPLACE_PRIVATE_SUBNET
export SERVICE_ACCOUNT=vm-runtime@"$PROJECT_ID".iam.gserviceaccount.com

gcloud config set project "$PROJECT_ID"
gcloud compute instances create dev-linux-01 \
  --project="$PROJECT_ID" \
  --zone="$ZONE" \
  --machine-type=e2-small \
  --subnet="$SUBNET" \
  --no-address \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --boot-disk-type=pd-balanced \
  --boot-disk-size=20GB \
  --boot-disk-auto-delete \
  --service-account="$SERVICE_ACCOUNT" \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --metadata=enable-oslogin=TRUE \
  --shielded-secure-boot \
  --shielded-vtpm \
  --shielded-integrity-monitoring \
  --labels=environment=dev,owner=REPLACE
```

Confirm the image family, zone, machine type, and org policy before running. `--no-address` prevents an external IPv4 address but does not prevent other routes/services from exposing the workload.

## Connect, use, and verify

```bash
gcloud compute instances describe dev-linux-01 --zone="$ZONE" \
  --format='yaml(status,networkInterfaces,serviceAccounts,shieldedInstanceConfig)'
gcloud compute ssh dev-linux-01 --zone="$ZONE" --tunnel-through-iap
```

IAP requires an IAM role and firewall ingress from `35.235.240.0/20` to the correct target on TCP 22. Enable OS Login and grant only the necessary OS Login role; use organization policy to prevent unmanaged SSH keys. Install/patch software using a controlled image or configuration-management pipeline; attach app permissions to the runtime service account. Send logs/metrics to Cloud Logging/Monitoring. Keep application state on appropriate durable services, not an unbacked boot disk.

Verify external IP is absent, service account IAM is narrow, shielded options are enabled, IAP-only admin path works, patch status and monitoring are healthy, and backup/restore is tested.

## Troubleshooting

- **IAP SSH denied:** user IAM/OS Login roles, IAP TCP forwarding role, IAP firewall source range/target, VM status, SSH daemon, and project/zone.
- **No outbound access:** subnet routes, Cloud NAT, egress firewall, DNS, and proxy; no external IP is expected.
- **App cannot access API:** attached service account, IAM binding on exact resource, API enablement, VPC Service Controls, and audit log.
- **Instance creation denied:** active project, API enablement, quota, zone capacity, org policy, subnet IP capacity, and exact permission.

## Stop and delete safely

Stop before deletion if you need to preserve boot-disk data; stopping may leave disk charges. Snapshot only approved data to a protected location. Confirm the exact instance and project, then delete the lab VM explicitly; inspect auto-delete settings, attached disks, static addresses, snapshots, firewall rules, and service-account permissions. Delete only resources owned by the lab. Budget alerts may arrive after charges accrue.
