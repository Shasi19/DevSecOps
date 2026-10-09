# Grafana dashboard and alert lifecycle

## 1. Onboard a datasource

Identify backend, auth method, network path, owner, query limits, retention, and data classification. Add the datasource through provisioning or controlled UI; use a scoped secret provider, never credentials in dashboard JSON/Git. Verify a small known query and permissions before sharing.

## 2. Design a dashboard around an operator task

Define audience and question. Place service health/error budget first; add rate, error ratio, latency, saturation, dependencies, and deployment markers. Use consistent units/legends, bounded variables and useful defaults. Link panels to logs/traces/runbooks. Avoid excessive panels, refresh intervals, or high-cardinality queries.

## 3. Provision and review

Store dashboard definitions and alert rules as code with stable UIDs/folder ownership. Validate JSON/YAML and datasource references in a test instance. Review permissions and provisioning ownership; do not use UI edits that will be overwritten without a promotion path.

## 4. Create and test alerts

Use an actionable query and reduce/threshold condition; set evaluation group/window, pending duration, no-data/error behavior, labels, contact point, notification policy, and runbook. Test firing/recovery and route with a test receiver before paging on-call. Group duplicate symptoms; do not silence permanently.

## 5. Incident use

Set incident time range; compare healthy/failing region/revision; follow traces/log links; annotate deploy/mitigation; capture relevant dashboard snapshot under data policy. An empty panel can mean no traffic, missing data, query error, or permissions—not zero.

## 6. Troubleshoot and retire

Datasource error: auth, DNS/TLS, plugin/version, query timeout. Slow panel: inspect query, interval, backend cardinality and refresh. Alert mismatch: rule expression/reducer, pending duration, labels, no-data config. On service retirement, disable routes, export/delete dashboards according to retention, and revoke datasource credentials.
