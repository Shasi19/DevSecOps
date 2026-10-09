# Grafana

## Mental model

Grafana visualizes and explores data from configured data sources such as Prometheus, Loki, Elasticsearch, and cloud monitoring systems. Dashboards contain panels, queries, variables, and annotations. Grafana is a presentation and alerting layer; source data quality and retention remain responsibilities of the underlying systems.

## Build useful dashboards

Start from a user or operator question, not a chart type. Put service health and SLO signals first; add drill-downs for traffic, errors, latency, and saturation. Use consistent units, clear titles, meaningful time ranges, and labels. Variables should narrow a dashboard safely and predictably. Avoid a single dashboard with hundreds of panels or high-cardinality selectors that overload the data source.

Provision data sources, dashboards, folders, and alert rules as code for repeatability. Use stable UIDs and review changes. Set panel query limits and refresh intervals based on data freshness and backend capacity. Annotations can correlate deployments and incidents, but should be trustworthy.

## Alerting and access

Write alerts against actionable conditions, specify pending windows and recovery behavior, and route them to an owner with context/runbooks. Avoid duplicate pages for the same incident. Use folders/teams and least-privilege roles; protect data-source credentials and restrict public dashboard sharing. A dashboard is not an alerting strategy by itself.

## Practice

Create an SLO dashboard with request rate, error ratio, and latency, then add a linked drill-down and one actionable alert. Provision it in a test instance and verify the alert with both firing and recovery data.

## Further reading

[Grafana documentation](https://grafana.com/docs/grafana/latest/)
