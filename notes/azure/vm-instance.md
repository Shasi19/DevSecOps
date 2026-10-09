# Azure Linux VM: purpose, creation, use, and cleanup

## What an Azure VM is for

Azure Virtual Machines provide OS-level control for legacy software, custom agents, specialized compute, or workloads that cannot use App Service, Functions, Container Apps, or AKS. A VM means you own guest OS hardening, patching, capacity, availability design, and recovery. For stateless production workloads use scale sets or managed services rather than one pet VM.

## Before creation

Use a sandbox subscription and approved Region; create or identify a VNet/subnet and narrowly scoped NSG; confirm quota/size availability; choose a supported patched image; decide identity, disk encryption, monitoring, patch owner, backup, and decommission date. Avoid a public IP and inbound SSH. Use Bastion or an approved private admin path.

## Create a private VM (instructional Azure CLI)

The following assumes the resource group, VNet, subnet, NSG, and SSH key are already reviewed. Do not run against production without an approved change and cost review.

```bash
az account show --output table
az account set --subscription "REPLACE-WITH-SANDBOX-SUBSCRIPTION"

az vm create \
  --resource-group rg-dev-lab \
  --name vm-dev-linux-01 \
  --location eastus \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username devopsadmin \
  --authentication-type ssh \
  --ssh-key-values "$HOME/.ssh/id_ed25519.pub" \
  --vnet-name vnet-dev \
  --subnet snet-private-vm \
  --nsg nsg-private-vm \
  --public-ip-address "" \
  --assign-identity \
  --os-disk-size-gb 32 \
  --tags environment=dev owner=REPLACE purpose=learning
```

CLI syntax/image SKU availability can vary; inspect `az vm create --help` and your subscription policy. Ensure the NSG allows only required traffic (for example, admin from Bastion subnet) and no Internet SSH. Use a managed identity rather than storing service credentials on disk.

## Use and verify

```bash
az vm show -g rg-dev-lab -n vm-dev-linux-01 \
  --show-details --query '{id:id,power:powerState,privateIp:privateIps,publicIp:publicIps}' \
  --output yaml
az vm identity show -g rg-dev-lab -n vm-dev-linux-01 --output yaml
```

Connect through Azure Bastion or an approved private management path. Apply OS updates, configure monitoring/Defender where applicable, and deploy app software through a repeatable image or configuration-management process. For resilient stateless services, use a Virtual Machine Scale Set across zones with health probes and rolling upgrades. Keep durable data in managed storage/database services.

Verify no public IP is assigned, identity has only intended roles, disk encryption and backup policies apply, patch/monitoring state is healthy, and a service-level check succeeds.

## Troubleshooting

- **SSH via Bastion fails:** validate Bastion state/subnet, target private IP, NSG source/destination rules, SSH daemon, local OS firewall, username/key, and route.
- **VM cannot access a private endpoint:** resolve DNS from the VM; inspect private DNS links, endpoint approval, UDR, NSG, service firewall, and identity authorization.
- **Provisioning failed:** check quota, SKU/zone availability, image, policy deny, subnet IP capacity, and Activity Log correlation ID.
- **Unexpected exposure:** inspect NIC public IP, NSG effective rules, load balancer, UDR, and host firewall; remove the path and inspect logs.

## Stop and delete safely

`az vm stop` deallocates compute; disks, snapshots, public IPs, and other resources may still incur charges. Before deletion, confirm the VM is lab-owned, preserve required data, understand OS/data disk delete settings, and identify dependent network resources. Delete the VM by its explicit name/ID only after review; do not remove a shared VNet/NSG or production backup. Check Cost Management after cleanup.
