# Prometheus metrics-to-alert process

## 1. Define the operational question

Choose the user/service behavior to observe: availability, request/error rate, latency, saturation, queue age, or dependency status. Define owner, labels, units, expected traffic, retention, and whether alert should page or ticket. Avoid collecting data without a use/retention owner.

## 2. Instrument

Expose `/metrics` over a restricted network path. Use counters for cumulative events, gauges for current values, histograms for distributions. Name metrics with units; choose bounded labels such as service/region/status class. Never label with user/request IDs, arbitrary URLs, or unbounded exception text.

## 3. Discover and scrape

Add static targets only for small stable setups; use service discovery for dynamic fleets. Configure scrape interval, timeout, TLS/auth, relabeling, and target labels. Restrict metrics endpoint access. Validate target health and sample labels before writing alerts.

```bash
promtool check config prometheus.yml
promtool check rules alerts.yml
```

## 4. Query and record

Start with raw selector and graph one target; inspect labels and counter resets. Apply `rate()`/`increase()` before aggregating counters. Use histogram bucket aggregation for cross-instance quantiles. Add recording rules for repeated expensive SLI queries, with review and test fixtures.

## 5. Alert and route

Alert on sustained user impact with `for`, meaningful labels, summary, service owner, and runbook. Configure Alertmanager grouping, inhibition, silences with expiry, and tested receiver. Test firing, recovery, no data, duplicate alerts, and notification failure. A scrape-down alert and application-availability alert answer different questions.

## 6. Operate Prometheus

Monitor scrape/evaluation failures, series/cardinality growth, WAL/storage, disk, memory, rule duration, remote-write backlog, and Alertmanager health. Define retention/backup/HA; local TSDB is not automatically durable long-term storage. Keep query/admin APIs private and credentials protected.

## Troubleshoot

Target down: DNS/TLS/auth/firewall/endpoint/timeout. Missing series: exporter instrumentation, relabeling, labels, range, scrape errors. Alert absent: rule loaded, evaluation, labels, no-data semantics, threshold. Sudden disk: cardinality labels, retention, target explosion, remote-write backlog.
