# ELK Stack: Elasticsearch, Logstash, and Kibana

## Mental model

Elasticsearch stores and searches indexed documents across shards and replicas. Logstash can collect, parse, and route events through input/filter/output pipelines. Kibana supports search, visualizations, dashboards, and alerting. Beats and Elastic Agent are common collection options. Current Elastic deployments may use integrated features beyond the original three-component stack.

## Data lifecycle

Define event schemas and timestamps before ingest. Parse at the edge or in a pipeline, normalize important fields, and remove secrets/irrelevant payloads. Use index templates and lifecycle policies for mappings, rollover, retention, and tiering. Mapping choices affect query behavior and storage; uncontrolled dynamic fields can create mapping explosion. Search by time and selective filters, then aggregate.

## Resilience and performance

Shards are parallelism and allocation units, not a universal performance knob. Choose shard sizes and replica count based on workload and recovery goals. Monitor cluster health, JVM/memory pressure, disk watermarks, indexing/search latency, and rejected tasks. Back up snapshots to a separate, protected repository and regularly test restore. A replica is not a backup.

## Security

Require authenticated TLS access, restrict roles and index privileges, protect API keys, and isolate public network exposure. Apply document/field access controls only when properly supported and tested. Manage retention and deletion for regulated data.

## Practice

Ingest JSON service logs, define a stable mapping, create a lifecycle policy, and build an error-rate dashboard. Simulate node loss and restore a snapshot in a separate environment.

## Further reading

[Elastic documentation](https://www.elastic.co/guide/index.html)

## Topic roadmap and data-flow diagram

**Ingest and query:** Elastic Agent/Beats or Logstash collect events; ingest pipelines parse/enrich; mappings define field types; indices/data streams organize data; shards distribute work; Kibana explores and visualizes. Use ECS-compatible fields when practical. Prefer data streams/lifecycle policies for time-series logs.

```mermaid
flowchart LR
  APP[Apps / hosts] --> AGENT[Agent or Beats]
  AGENT --> PIPE[Logstash / ingest pipeline]
  PIPE --> ES[Elasticsearch data stream]
  ES --> KIB[Kibana search + dashboards]
  ES --> SNAP[Protected snapshots]
```

**Example:** parse JSON at ingestion, map `@timestamp` as date and status as numeric/keyword as appropriate, redact secrets, and configure rollover/retention before high-volume onboarding. Aggregations should filter time and fields first.

**Troubleshooting:** cluster yellow—unassigned replicas, capacity and allocation; red—unassigned primary and data risk; indexing rejected—resource pressure, bulk sizing, mappings; query slow—shard count, expensive wildcard/aggregation, time range; disk watermark—retention, snapshots, tiering and expansion. Restore a snapshot into an isolated test cluster.

**Revision:** primary shard stores a partition; replica supports resilience/read capacity; replica is not backup; mapping controls query semantics; lifecycle manages data; snapshot repository must be protected and restore-tested; Kibana is not a substitute for access controls.
