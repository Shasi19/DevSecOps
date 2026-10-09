# Azure for DevOps

## Mental model

Azure resources live in subscriptions and are organized with management groups and resource groups. A resource group is a lifecycle/administrative grouping, not a network or security boundary by itself. Regions, availability zones, and paired-region strategies inform resilience choices.

## Core building blocks

- **Identity and governance:** Microsoft Entra ID, managed identities, role-based access control (RBAC), Azure Policy, and subscription/resource locks.
- **Networking:** virtual networks, subnets, network security groups, private endpoints, DNS, and load-balancing services.
- **Compute and data:** Virtual Machines, App Service, Functions, AKS, Storage, and managed database offerings.
- **Operations:** Azure Monitor, Log Analytics workspaces, alerts, Activity Logs, and Resource Health.

## Delivery workflow

Use Bicep or Terraform to provision environments consistently. Authenticate automation with workload identity federation or managed identities where supported; avoid client secrets that never expire. Build and scan immutable images/packages, promote the same artifact through stages, and deploy with health probes plus a rollback path. Keep production approvals and identity permissions separate from ordinary build permissions.

## Security and reliability

Apply least-privilege RBAC at the narrowest sensible scope, review inherited assignments, and use Policy to prevent unsafe configurations. Prefer private connectivity for sensitive services. Monitor both application SLIs and platform health. Backups need retention, isolation, and restore tests; zone redundancy and geo-replication have service-specific constraints and costs.

## Practice

Create a small web service with a managed identity, private data access, centralized diagnostics, and an alert on failed requests. Use policy to require tags and secure transport. Demonstrate a redeploy and a restore, then trace which identity can read secrets and modify the production network.

## Further reading

[Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/) · [Azure RBAC](https://learn.microsoft.com/azure/role-based-access-control/overview)
