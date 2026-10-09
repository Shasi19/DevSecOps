# AWS delivery, observability, and recovery lab

> Use a dedicated sandbox account. Load balancers, NAT gateways, databases, logging, and data transfer can incur ongoing costs. Check the current AWS Pricing Calculator and delete only lab-owned resources.

## Delivery pattern

1. CI obtains short-lived AWS credentials through OIDC and assumes a narrowly scoped role.
2. Build, test, scan, and sign an immutable artifact; store it in a private ECR repository.
3. Deploy the exact image digest to a non-production service.
4. Verify health and SLO telemetry; use canary/linear rollout where supported.
5. Require protected production approval; retain a known-good revision for rollback.

Keep build role, deploy role, and workload runtime role separate. Protect GitHub/GitLab/Jenkins environment gates; do not expose production credentials to arbitrary PR code.

## Observability

CloudWatch metrics/logs/alarms cover operational signals; CloudTrail covers API/control-plane activity; VPC Flow Logs support network analysis; X-Ray/OpenTelemetry traces explain request paths. Define retention, access, redaction, and cost. Alert on user impact, not every resource metric. Record deployment markers.

## Recovery design

For every stateful resource specify backup method, account/Region, encryption key recovery, retention/immutability, RPO/RTO, and restore owner. Isolate backup permissions from production administrators where possible. A Multi-AZ standby or read replica is not an independent backup. Run restore exercises and record measured results.

## Incident scenario: unhealthy deployment

Freeze promotion; compare deployment version/time with error, latency, saturation, and dependency signals. Confirm target health and scaling capacity. Roll back to the previous immutable digest if the new revision caused impact and schema compatibility permits. Validate user traffic and data integrity; preserve CloudTrail/deployment logs; perform a blameless review and track preventive work.

## Lab acceptance

- A private workload can access only required data/service endpoints.
- Public ingress reaches the approved load balancer and no direct workload address.
- CI can deploy only to its intended environment; untrusted branches cannot assume production role.
- An alarm reaches an owned response route and points to a runbook.
- A backup restores into an isolated target within the stated objective.
