# OCI Compute instance: purpose, creation, use, and cleanup

## What an OCI Compute instance is for

Use Compute when an application needs guest OS control, a custom agent/runtime, legacy compatibility, or a specialized shape. For containers evaluate OKE or Container Instances; for managed database/application capabilities prefer the managed service where it meets requirements. VMs require patching, capacity, access control, backup, and availability planning.

## Before launch

Choose a sandbox compartment and Region; verify shape/image support and quotas. Prepare a private subnet, route table, NSG/security list, DNS, and a management path through OCI Bastion or approved private access. Define a dynamic group/instance principal if the workload needs OCI APIs; use least-privilege policy. Decide boot-volume encryption/backup, monitoring, patch owner, and teardown date. Do not assign a public IP by default.

## Launch a private instance (instructional OCI CLI)

OCI CLI commands and shape/image requirements depend on Region and tenancy. Resolve the image OCID for the chosen Region and architecture first; replace every placeholder. Review the complete launch request before executing in a sandbox.

```bash
export TENANCY_OCID=ocid1.tenancy.oc1..REPLACE
export COMPARTMENT_OCID=ocid1.compartment.oc1..REPLACE
export SUBNET_OCID=ocid1.subnet.oc1..REPLACE_PRIVATE_SUBNET
export IMAGE_OCID=ocid1.image.oc1.REGION.REPLACE
export AD_NAME=REPLACE_AVAILABILITY_DOMAIN

oci compute instance launch \
  --compartment-id "$COMPARTMENT_OCID" \
  --availability-domain "$AD_NAME" \
  --display-name vm-dev-01 \
  --shape VM.Standard.E5.Flex \
  --shape-config '{"ocpus":1,"memoryInGBs":8}' \
  --image-id "$IMAGE_OCID" \
  --subnet-id "$SUBNET_OCID" \
  --assign-public-ip false \
  --ssh-authorized-keys-file "$HOME/.ssh/id_ed25519.pub" \
  --wait-for-state RUNNING
```

The image and shape must be compatible. A subnet argument must refer to the intended subnet; confirm route and security policy before use. Use an OCI Bastion session for administration rather than allowing public SSH. For API access, attach the intended dynamic-group rule/policy and verify the principal is the instance actually launched.

## Use and verify

```bash
oci compute instance list \
  --compartment-id "$COMPARTMENT_OCID" \
  --display-name vm-dev-01 \
  --query 'data[].{id:id,state:"lifecycle-state",name:"display-name"}'
oci compute instance get --instance-id ocid1.instance.oc1..REPLACE
```

Inspect VNIC attachments/private IP, subnet, NSGs, route table, boot-volume encryption/backup policy, and monitoring. Connect using Bastion or an approved private path. Apply OS updates and workload configuration through an image pipeline/Ansible; do not keep static API signing keys on the host. Put durable application data on an intentionally selected database/storage service.

## Troubleshooting

- **Bastion cannot connect:** session target/private IP, Bastion policy, subnet route, NSG and Security List ingress, host firewall, SSH daemon/user/key.
- **Instance cannot call Object Storage:** instance principal/dynamic-group match, policy scope/verbs, Service Gateway route, DNS, NSG egress, and Audit error.
- **Launch fails:** image/shape compatibility, AD availability, compartment permission, quota, subnet capacity, and request ID.
- **Backend unhealthy:** load balancer NSG paths, listener/probe configuration, app bind address/port, and health response.

## Stop, preserve, and terminate

Stopping does not necessarily stop boot/block volume or other resource charges. Back up required data and confirm retention before terminating. Review the exact OCID and compartment. Termination may delete the boot volume depending on the request; preserve only when required and account for ongoing charges. Do not remove shared subnets, NSGs, gateways, Vault keys, or backups. Verify termination and review cost by compartment/tag afterward.
