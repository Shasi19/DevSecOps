# Dynatrace observability onboarding process

## 1. Plan scope and data

Choose service/team/environment boundaries, host/process coverage, custom telemetry, retention, privacy classification, network egress/proxy, and token owner. Map telemetry to a service catalog and define user-facing SLIs before adding alerts.

## 2. Onboard a canary

Use approved deployment automation for OneAgent or supported integration. Scope permissions/API tokens narrowly. Start with one non-production host/service; verify agent version/health, process detection, service naming, topology, log/trace linkage, and resource overhead. Do not expose tenant endpoints broadly.

## 3. Expand and govern

Roll out by environment/host group with change window and rollback. Use tags/management zones consistently for ownership and access. Apply capture/privacy rules and retention. Review unsupported/ignored process detection and telemetry gaps.

## 4. Build operational views

Create service dashboards for traffic/errors/latency/saturation and key dependencies. Add deployment events. Configure alert profile based on SLO, with owner/runbook and deduplication. Test in a non-production environment; review false positives/negatives with on-call.

## 5. Incident workflow

Confirm affected user journey, timeframe, service/version/region, and telemetry completeness. Correlate problem events, traces, logs, infrastructure saturation, and deploy marker. Mitigate using reversible action, then verify SLI recovery. Record data gaps and remediation.

## Troubleshoot

Agent missing: host service, version, egress/proxy, token/cert, firewall. Service absent: process detection, filters, naming, OneAgent coverage. Alert storm: threshold, baseline, correlation, routing. Unusual bill/data volume: ingest/capture configuration, retention, high-cardinality custom dimensions.

## Offboard

Remove agent/integration through configuration management, revoke tokens, close network routes, remove ownership/alert routes, retain required audit data, and confirm the entity no longer reports. Do not merely hide a broken entity.
