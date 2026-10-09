# Prometheus monitoring

## Mental model

Prometheus periodically scrapes HTTP endpoints that expose time-series samples. A series is identified by its metric name and label set. Prometheus stores samples locally and evaluates PromQL queries and alerting rules. Labels are powerful dimensions but unbounded values (user IDs, request IDs) create dangerous cardinality growth.

## Instrumentation and querying

Use counters for cumulative events, gauges for values that rise and fall, histograms for distributions, and summaries only when their trade-offs fit. Name metrics consistently and include units. Prefer labels with small, known value sets. Query rates from counters with `rate()` over an appropriate range; aggregate only after applying rate to each original counter series. Histograms enable bucket-based quantile estimates across instances.

Configure scrape targets, service discovery, relabeling, retention, and remote storage deliberately. Validate targets and rules before production. Avoid treating missing data as zero without understanding the distinction. Alert on user-visible symptoms and sustained conditions, then attach a runbook and owner.

## Reliability and security

Prometheus is not a high-availability or long-term archive by default. Plan replication/remote write and backup according to the deployment. Restrict access to query/admin endpoints and protect scrape credentials. Monitor Prometheus itself: scrape failures, ingestion, rule evaluation, disk use, and cardinality.

## Practice

Instrument a service with request count, error count, and latency histogram. Build queries for error ratio and latency, create an actionable alert, and demonstrate how a high-cardinality label can inflate series count.

## Further reading

[Prometheus documentation](https://prometheus.io/docs/introduction/overview/) · [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/)
