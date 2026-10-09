# Prometheus config lab

The app target and metric names are placeholders. Before loading the config, replace them with the correct service-discovery target and instrumentation schema.

```bash
promtool check config prometheus.yml
promtool check rules alerts.yml
```

For realistic tests, add `promtool test rules` fixtures that cover normal traffic, sustained errors, low/no traffic, missing targets, and counter resets. Choose alert windows/thresholds from service SLO and traffic characteristics. The example runbook URLs use the reserved `.invalid` domain intentionally; replace them before routing notifications.
