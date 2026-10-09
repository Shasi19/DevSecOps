# Splunk for operations

## Mental model

Splunk indexes machine data and supports search, dashboards, and alerting through SPL (Search Processing Language). Events have timestamps and fields; parsing and field extraction determine how effectively data can be searched. Ingest volume, retention, and index design have operational and cost consequences.

## Search workflow

Start with a narrow time range and index/source constraints, then progressively filter and extract fields. Use `stats`, `timechart`, and `eval` for aggregation and transformation. Filter early to reduce work. Validate event timestamps, timezone, sourcetype, and field extraction when searches appear empty or inaccurate. Saved searches and dashboards should encode useful operational questions.

## Data onboarding and alerts

Normalize event structure and field names where possible. Avoid indexing duplicate or unnecessary data; redact secrets and personal data before ingestion. Monitor forwarders, parsing queues, indexing latency, and license/ingest usage. Alerts should have meaningful thresholds, suppression/throttling where appropriate, an owner, and a runbook. Distinguish missing telemetry from a true zero.

## Security and reliability

Use role-based access, least privilege, protected credentials, and audited administrative actions. Define retention and access according to data classification. Back up configuration and test recovery. Search workloads can affect shared capacity; use efficient time bounds and avoid expensive broad searches during incidents.

## Practice

Ingest sample application logs, validate timestamps and fields, create a dashboard for error rate and top failing endpoints, and alert on a sustained increase. Confirm secrets are redacted and the alert links to the right runbook.

## Further reading

[Splunk documentation](https://docs.splunk.com/Documentation)

## Topic roadmap and SPL example

```mermaid
flowchart LR
  SRC[Applications / hosts] --> FWD[Forwarder / HEC]
  FWD --> PARSE[Parsing + timestamp]
  PARSE --> IDX[Indexers]
  IDX --> SEARCH[Search head + SPL]
  SEARCH --> DASH[Dashboard / alert]
  DASH --> TEAM[Owning operator]
```

**Data flow:** forwarders/HEC receive events; parsing assigns timestamps, host, source, and sourcetype; indexers store searchable data; search heads execute SPL; dashboards/reports/alerts present results. Index-time and search-time processing have different cost and flexibility trade-offs. Validate timestamp extraction/timezone before tuning searches.

```spl
index=app sourcetype=service:json earliest=-15m
| stats count as requests count(eval(status>=500)) as errors by service
| eval error_pct=100*errors/requests
| sort - error_pct
```

Constrain index, sourcetype, and time early. Use `timechart` for trends, `stats` for aggregation, `eval` for derived fields, and joins/lookups selectively because they can be expensive. Redact credentials/PII before indexing and keep retention aligned to purpose and policy.

**Troubleshooting:** no events—forwarder/HEC connectivity, index permission, timestamp, source/sourcetype; search too slow—time bound, selective filters, cardinality, joins and index design; alert noisy—threshold/window, scheduling, suppression and missing data; ingest unexpectedly high—duplicate sources, verbose logs, sampling policy, and field bloat.

**Revision:** event parsing defines fields/time; SPL filters then transforms; ingestion volume drives storage/cost; search permissions and index permissions differ; alerts need owner/action; missing telemetry must not be read as zero.

## SPL runbook snippets

**Error count by service, bounded to recent data:**

```spl
index=app sourcetype=service:json earliest=-15m
| stats count(eval(status>=500)) as errors count as requests by service
| eval error_ratio=if(requests>0, errors/requests, null())
| where error_ratio > 0.05
| sort - error_ratio
```

**Find ingest gaps:** compare `tstats` event volume by host/sourcetype over equal windows against a known baseline; validate `_time` and ingestion-time lag before paging. Use index-time constraints and role permissions intentionally.

Before alerting, test expected event volume, no-data behavior, delayed events, duplicates, and DST/timezone boundaries. Set throttling/suppression only if it will not hide a distinct customer impact. Add owner and runbook URL to saved-search alert configuration.
