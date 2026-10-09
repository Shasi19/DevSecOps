# Dynatrace observability

## Mental model

Dynatrace combines telemetry collection, topology/context, analytics, dashboards, and alerting. OneAgent-based discovery can associate processes and services, while integrations and APIs extend coverage. Automatic correlation is useful, but teams still need to validate instrumentation, service boundaries, and data quality.

## Practical workflow

1. Define the service and its user-facing indicators before onboarding hosts.
2. Deploy agents or integrations through controlled automation and verify coverage.
3. Map services and dependencies; confirm names and ownership match the operating model.
4. Build dashboards and alerts around latency, traffic, errors, saturation, and business impact.
5. Correlate deployments and changes with incidents; review false positives and blind spots.

Use management zones/tags to organize views and permissions. Apply data capture controls and retention settings so sensitive data is not collected unnecessarily. Instrument custom events and metrics with stable, low-cardinality dimensions. Set alert thresholds based on service objectives and baseline behavior, not every metric fluctuation.

## Governance and operations

Protect API tokens, scope them narrowly, and rotate them. Manage agent rollout, upgrades, resource overhead, and network egress. Document ownership for dashboards, alert profiles, and integrations. Validate that disabled/instrumentation gaps are visible; a quiet dashboard may indicate missing data rather than a healthy service.

## Practice

Onboard a sample service, confirm its dependency map, create a latency/error dashboard, and configure an alert tied to a runbook. Introduce a deployment event and trace how it appears during a simulated incident.

## Further reading

[Dynatrace documentation](https://docs.dynatrace.com/)
