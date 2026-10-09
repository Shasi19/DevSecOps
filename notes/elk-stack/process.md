# ELK log pipeline lifecycle

## 1. Define schema and retention

Agree on event fields (`@timestamp`, service, environment, host, severity), types, UTC semantics, maximum event size, redaction, ingest volume, owner, retention, and search access. Decide ECS alignment and index/data-stream strategy before production ingestion.

## 2. Secure cluster

Use supported Elastic version, TLS, authentication, least-privilege roles, private networking, protected admin access, disk/JVM sizing, replica/zone settings, and snapshot repository. Backups must be separate and restore-tested. Never put admin credentials in Logstash pipeline text.

## 3. Ingest and parse

Deploy Elastic Agent/Beats or Logstash with authenticated TLS. Test pipeline against representative events; validate timestamps, field types, redaction, malformed event routing, and duplicate behavior. Apply index templates/lifecycle before high volume. Watch ingest rejections and mapping growth.

## 4. Build Kibana views and alerts

Use time-filtered searches, saved queries, dashboards with clear units, and alerts on actionable symptoms. Restrict spaces/data views by role. Link alerts to runbooks. Test no-data, delayed ingestion, and source outages.

## 5. Operate and recover

Monitor cluster health, shard allocation, disk watermarks, heap, indexing/search latency, ingest pipelines, lifecycle execution, and snapshots. For disk pressure, halt unbounded ingest, inspect retention and top indices, verify snapshot, then scale or expire approved data. Do not delete primary indices blindly.

## 6. Retire and restore

Stop source collection, revoke credentials, preserve required data, expire/delete only per retention/legal policy, remove pipelines/alerts, and verify volume drops. Restore snapshots into isolated cluster, validate mappings/doc counts/search, then cut over with an explicit rollback.
