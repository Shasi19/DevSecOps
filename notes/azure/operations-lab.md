# Azure delivery and production operations lab

> Use a dedicated sandbox subscription and check current service pricing/quotas. Budgets notify but are not guaranteed spending caps. Clean up only resources created for this lab.

## Architecture and delivery

Use Bicep/Terraform for a resource group, VNet, workload, identity, and monitoring. CI authenticates through federated workload identity with trusted repo/branch/environment conditions. Build and scan once, publish to ACR by immutable digest, deploy to staging, check health, and promote through an environment approval. Avoid storing Azure client secrets in CI.

## Operations setup

- Enable Activity Log export and relevant resource diagnostic settings.
- Build dashboards for request rate, error ratio, latency percentiles, saturation, and dependency health.
- Alert on actionable SLO symptoms; include ownership and runbook links.
- Set log retention/access and redact secrets/PII.
- Define backup, restore, failover, and key recovery procedures; test in an isolated target.

## Incident scenario: private endpoint connection fails

Confirm DNS resolves to the expected private IP from the workload; verify private DNS zone link/records; inspect subnet route/NSG/firewall; confirm private endpoint approval; check service public-network/firewall policy; then inspect managed identity/data-plane authorization. Capture correlation IDs and diagnostic logs. Network reachability and permission are separate failure domains.

## Release and recovery exercise

Deploy version A, verify SLI and data path, then deploy a deliberately unhealthy staging revision. Ensure health gates prevent promotion; route back to A; check schema compatibility and telemetry. Simulate data restore to a separate resource group/subscription and measure achieved RPO/RTO.

## Readiness gates

Identity has least privilege; no public data endpoint unless required; private DNS and egress tested; CI trust claims constrained; release artifact immutable; alert owner/runbook known; backup restoration evidenced; cost and teardown ownership recorded.
