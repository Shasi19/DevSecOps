# Splunk source-to-alert process

## 1. Define event contract

For each source specify owner, source/sourcetype, timestamp/timezone, required fields, volume estimate, redaction, index, retention, access role, and incident use. Remove secrets/PII at source where possible. Do not onboard unbounded debug logs by default.

## 2. Onboard source

Select supported forwarder, HEC, or cloud integration. Use TLS, scoped tokens/certs, network allowlists, and managed secret storage. Validate source connectivity and event delivery in a test index. Check duplication, parsing latency, queue backpressure, and timezone.

## 3. Parse and normalize

Define timestamp extraction, sourcetype, host/source, field names/types, and redaction. Test representative valid, malformed, multiline, late, and oversized events. Prefer search-time extraction unless there is a measured reason for index-time parsing. Set volume controls and index retention.

## 4. Build search and dashboard

Constrain index/sourcetype/time range first; validate counts against source-of-truth. Use `stats`/`timechart`, explicit null/no-data semantics, and controlled lookups. Save searches/dashboard with ownership and version history.

## 5. Alert and operate

Set meaningful evaluation window, threshold, schedule, suppression/throttling, owner, runbook, and notification route. Test normal/firing/recovery/no-data cases and delayed events. Monitor ingest volume, license/entitlement, parsing queues, forwarder health, and search latency.

## Troubleshooting

No data: forwarder/HEC, token, index permission, timestamp, source/sourcetype/time bounds. Duplicate: multiple collection paths, replay. Slow query: broad time/index, high cardinality, joins/lookups. Alert missing: search schedule, owner permissions, suppression, no-data, notification endpoint.

## Retire source

Disable collection at source, revoke HEC/API credentials, remove routing/parsing configs after retention review, preserve required indexes, remove alert dependencies, and confirm ingest volume falls.
