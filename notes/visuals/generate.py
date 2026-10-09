#!/usr/bin/env python3
"""Generate original, topic-specific SVG and PNG study cards for the guide set."""

from __future__ import annotations

import html
import subprocess
from pathlib import Path

from PIL import Image

NOTES = Path(__file__).resolve().parents[1]
ARCHETYPES = (
    ("SYSTEM MAP", "Follow a request through its trust and service boundaries."),
    ("WORKFLOW", "Make each transition explicit; verify the outcome before proceeding."),
    ("SECURITY", "Apply least privilege at the boundary, then audit the action."),
    ("DELIVERY", "Promote one immutable change through gated environments."),
    ("OBSERVABILITY", "Connect the signal to an owner, a threshold, and an action."),
    ("DIAGNOSIS", "Start with evidence; isolate one failing layer at a time."),
    ("RECOVERY", "Stabilize first, restore from a known-good point, then verify."),
    ("RESILIENCE", "Remove single points of failure and rehearse the fallback."),
    ("SCENARIO", "Communicate impact, owner, next update, and a measurable exit."),
    ("REVISION", "Remember the control, its evidence, and the failure it prevents."),
)

# Each guide has ten original, domain-specific flow examples:
# title | four connected steps | production check.
DATA = {
    "aws": ("AWS CLOUD", "#f6a64a", """Request path|Route 53 > CloudFront/WAF > ALB > private EC2 > RDS|Keep application instances private; terminate public traffic at the edge.
Instance lifecycle|AMI and subnet > launch template > Auto Scaling Group > health check|Pin a reviewed AMI and use instance roles instead of static keys.
Identity boundary|Identity Center role > permission set > STS session > CloudTrail event|Grant temporary, scoped access and review the resulting audit trail.
Network segmentation|VPC route table > public ALB subnet > private app subnet > isolated data subnet|Check both route tables and security groups; a private subnet has no direct internet route.
Infrastructure delivery|Terraform module > remote locked state > reviewed plan > controlled apply|Use separate state boundaries and reject unreviewed destructive plans.
Service health|CloudWatch metrics > SLO alarm > SNS/on-call > runbook action|Alert on user-visible symptoms and test the notification path.
Access failure|Caller identity > role trust > permission policy > resource policy|Distinguish authentication, trust, identity-policy, and resource-policy failures.
Regional recovery|Route 53 health check > secondary region > replicated data > failover test|Document replication lag and verify recovery objectives with a timed exercise.
Incident response|Detect 5xx rise > scope AZ and dependency > shift traffic > confirm recovery|Set one incident lead, preserve evidence, and communicate customer impact.
Quick revision|IAM least privilege > private-by-default network > encrypted data > observable change|Every privileged action should be attributable, time-bounded, and reviewable."""),
    "azure": ("MICROSOFT AZURE", "#57b9ef", """Request path|Azure DNS > Front Door/WAF > Application Gateway > private VM scale set > data tier|Use health probes and keep the origin inaccessible from the public internet.
VM lifecycle|Image and VNet > NIC/NSG > VM or scale set > Azure Monitor health|Prefer managed images, managed identity, and private administration.
Identity boundary|Entra ID group > Azure RBAC role > managed identity > Activity Log|Assign roles at the narrowest practical scope and review inherited access.
Network segmentation|Hub firewall > spoke subnet > NSG rules > private endpoint|Validate effective routes and NSG flow; private endpoint DNS must resolve privately.
Infrastructure delivery|Bicep/Terraform > remote state > plan/what-if > gated deployment|Separate subscriptions and protect state, approvals, and production credentials.
Service health|Azure Monitor metric > alert rule > action group > owned response|Exercise the action group and ensure alerts identify the affected resource.
Access failure|Sign-in log > token/role scope > resource provider > diagnostic setting|Check role propagation, scope, deny assignments, and provider registration.
Regional recovery|Zone-redundant service > geo-replicated data > paired-region plan > failover drill|State RPO/RTO, replication mode, and failback owner before an outage.
Incident response|Alert on latency > identify dependency > mitigate traffic > validate SLO|Keep a single incident timeline and communicate next-update time.
Quick revision|Entra identity > scoped RBAC > private endpoints > policy and logs|A private link is not authorization; keep identity and network controls separate."""),
    "gcp": ("GOOGLE CLOUD", "#52c89a", """Request path|Cloud DNS > HTTPS Load Balancer > serverless NEG > Cloud Run > Cloud SQL|Use a supported private service path and restrict ingress at the service boundary.
Compute lifecycle|Hardened image > instance template > managed instance group > health check|Use OS Login/IAM and avoid broad SSH ingress from the internet.
Identity boundary|Google group > IAM role > service account identity > Cloud Audit Logs|Grant roles to principals at the smallest useful resource scope.
Network segmentation|VPC route > proxy-only/load-balancer subnet > private workload > private service access|Check routes, firewall direction, and DNS before diagnosing application access.
Infrastructure delivery|Terraform module > remote state bucket > reviewed plan > federated CI apply|Use workload identity federation and state locking/versioning.
Service health|Cloud Monitoring SLI > alert policy > notification channel > runbook|Alert on customer-facing latency and error budget burn, not noisy host symptoms.
Access failure|Active principal > IAM policy > service account impersonation > API audit log|Check the actual active account and inherited policy before changing roles.
Regional recovery|Regional service > cross-region data copy > traffic steering > rehearsed failover|Measure replication lag and validate recovery against declared RPO/RTO.
Incident response|SLO alert > trace critical path > mitigate dependency > confirm good traffic|Use logs, metrics, and traces together; capture a decision and owner for each action.
Quick revision|IAM roles > private IP and IAP > managed services > audit and SLOs|IAP access requires both IAM authorization and an allowed network path."""),
    "oci": ("ORACLE CLOUD", "#e66b6f", """Request path|DNS/WAF > public load balancer > private app subnet > private database subnet|Keep backend VNICs private and allow only required listener-to-backend ports.
Compute lifecycle|Reviewed image > compartment and subnet > instance launch > health and patching|Use instance principals or approved keys; avoid public admin access.
Identity boundary|Identity domain group > compartment policy > dynamic group > audit event|Scope policy statements to the intended compartment and resource type.
Network segmentation|VCN route table > public LB subnet > private compute subnet > DB subnet|Check security lists and NSGs together; inspect the effective route and gateway.
Infrastructure delivery|Terraform provider > protected state > reviewed plan > approved apply|Pin provider versions and protect state and OCI credentials.
Service health|Monitoring metric > alarm destination > on-call runbook > verified mitigation|Test alarm delivery and include compartment, resource, and response owner.
Access failure|CLI profile/principal > IAM policy > compartment scope > service audit log|Confirm the selected region, tenancy, profile, and compartment before editing policy.
Regional recovery|Availability domain/fault domain > backup copy > alternate region > recovery test|Back up boot and data volumes and rehearse restoration with measured RTO.
Incident response|Customer symptom > LB/backend health > subnet/security path > recovery check|Separate control-plane access issues from instance and application failures.
Quick revision|Compartments > least-privilege policy > private VCN > alarms and backups|A compartment organizes and scopes resources; it does not replace network controls."""),
    "linux": ("LINUX OPERATIONS", "#b79cff", """Host request path|systemd unit > listening socket > firewall rule > application dependency|Confirm the service is listening on the expected interface and port.
Safe change lifecycle|Baseline > scoped config edit > syntax check > controlled reload|Keep a rollback copy and validate configuration before restarting a critical service.
Privilege boundary|User/group > sudo policy > file ownership > audited command|Use named accounts, narrow sudo rules, and least-privilege file permissions.
Patch rollout|Package repository > staging host > canary batch > verified fleet|Check kernel/reboot requirements and monitor each rollout batch.
Host observability|journald/syslog > metrics and disk > alert threshold > runbook|Include time range, unit name, and host identity in every incident query.
Process diagnosis|User symptom > process/resource check > socket/dependency check > focused fix|Capture `journalctl`, `systemctl`, and resource evidence before restarting.
Disk recovery|Filesystem usage > largest path > retention/rotation > free-space verification|Do not delete open files blindly; check inode usage and application retention.
Service resilience|systemd restart policy > readiness check > dependency timeout > tested recovery|A restart policy is not a substitute for fixing a crash loop or bad dependency.
Scenario: failed deploy|Change timestamp > unit status > config validation > rollback and health probe|Preserve logs and state the impact, rollback trigger, and recovery evidence.
Quick revision|Process > socket > logs > resource limits|Verify from the layer nearest the user outward; avoid speculative permission changes."""),
    "git": ("GIT WORKFLOW", "#f06f8e", """Change path|Issue and acceptance criteria > focused branch > reviewable commits > merged change|Keep a small diff with tests and an explicit rollback/revert strategy.
Branch lifecycle|Sync base > create topic branch > commit > rebase/merge by policy|Inspect status before switching and never rewrite shared history casually.
History safety|Working tree > index > commit object > remote reference|Use `git diff --cached` to review exactly what will enter the commit.
Secret defense|Pre-commit scan > push protection > CI secret scan > rotate and purge response|Revoking a leaked credential is urgent; deleting a line alone does not revoke it.
Release flow|Signed/tagged commit > CI build > immutable artifact > promoted deployment|Deploy the same artifact digest that passed tests.
Conflict diagnosis|Conflict markers > inspect both intents > resolve > test and continue|Do not accept an entire side blindly; verify the resulting diff.
Recovery path|Reflog entry > identify lost commit > create rescue branch > verify content|Reflog entries expire; recover promptly and avoid destructive cleanup.
Team resilience|Protected default branch > required checks > CODEOWNERS > reviewed merge|Require checks that are deterministic and match the protected target branch.
Scenario: bad commit|Stop rollout > revert the introducing commit > rerun checks > verify service|A revert creates an auditable inverse change without rewriting shared history.
Quick revision|Working tree > index > commit > remote|`reset`, `restore`, and `revert` have different effects; inspect before acting."""),
    "github": ("GITHUB", "#90a6ff", """Pull request path|Issue and branch > commit checks > review/approval > protected merge|Require current checks and review on the exact commit being merged.
Repository setup|Create repo > default branch policy > CODEOWNERS > security features|Restrict who can bypass rules and keep ownership aligned with team changes.
Identity boundary|Human/robot identity > scoped token or app > repository permission > audit log|Prefer short-lived GitHub App or OIDC credentials over long-lived PATs.
Release supply chain|Tag/release > workflow build > provenance/attestation > signed artifact|Pin actions to immutable commit SHAs and protect release permissions.
Security signal|Dependabot/secret scan > alert triage > owner and SLA > verified remediation|Confirm the fixed version and rerun the relevant scan after changing dependencies.
Workflow diagnosis|Event and ref > job permission > runner environment > artifact/log evidence|Check the triggering event and token permissions before changing a workflow.
Credential response|Revoke credential > identify exposure window > rotate consumers > review audit|Treat a published secret as compromised even if the repository is private.
Delivery resilience|Protected branch > reproducible CI > retained artifact > rollback release|Keep release artifacts available and document a tested rollback path.
Scenario: failing check|Find failing job > reproduce command > fix root cause > rerun exact commit|Never merge by bypassing a failing security or correctness check.
Quick revision|Branch protection > least privilege > immutable dependencies > auditable releases|Repository permissions and workflow token permissions are separate controls."""),
    "github-actions": ("GITHUB ACTIONS", "#53c9c2", """Workflow path|Pull request event > lint/test jobs > protected environment > deploy job|Grant write/deploy permissions only to the job that needs them.
Workflow authoring|Choose event/ref > define jobs > pin actions > add explicit permissions|Use least-privilege `permissions` and avoid executing untrusted PR code with secrets.
Identity boundary|GitHub OIDC token > cloud trust condition > short-lived role > cloud audit|Restrict issuer, audience, repository, branch/environment claims.
Artifact promotion|Build once > test digest > attest/provenance > deploy same artifact|Avoid rebuilding different bytes in production after testing.
Operational signal|Job duration/failure > annotation and summary > owner alert > runbook|Make failures actionable and retain logs/artifacts only as long as needed.
Workflow diagnosis|Event payload > expression/ref > permission denial > runner log|Inspect the expanded event context and job token scopes before changing YAML.
Secret response|Disable compromised secret > rotate provider credential > audit runs > verify consumers|Use OIDC where possible and avoid printing secrets through shell tracing.
Runner resilience|Ephemeral runner > isolated job > cache boundary > autoscaled capacity|Do not share a privileged persistent runner with untrusted workloads.
Scenario: deploy went wrong|Stop promotion > identify artifact and environment > rollback > verify health|Protect production environments with reviewers and deployment concurrency.
Quick revision|Triggers > jobs > permissions > artifacts|A workflow file is executable supply-chain code; review action pins and scopes."""),
    "gitlab": ("GITLAB", "#f08b5b", """Merge request path|Feature branch > pipeline rules > approval > protected merge|Require pipeline success and approval for the current source revision.
Pipeline setup|Stages/jobs > runner tags > cache/artifact contract > rules|Distinguish cached dependencies from immutable artifacts passed between jobs.
Identity boundary|Protected environment > scoped CI variable/OIDC > deploy role > audit event|Masking is not a safety boundary for malicious pipeline code; restrict who can change it.
Release path|Build image > scan and test > sign/digest > promote to environment|Use the tested image digest instead of rebuilding during deployment.
Pipeline signal|Job status > test/scan reports > alert owner > tracked remediation|Publish security reports in native formats and assign findings to an owner.
Pipeline diagnosis|Pipeline source > rules evaluation > runner assignment > job trace|Check whether rules skipped the job before debugging runner capacity.
Secret response|Revoke token > audit logs/jobs > rotate dependencies > verify new identity|Protect variables and avoid exposing them to fork or untrusted MR pipelines.
Runner resilience|Isolated runner > autoscaling capacity > bounded retries > cleanup|Prefer ephemeral isolated runners for workloads with different trust levels.
Scenario: stuck deployment|Inspect environment lock > verify active job > cancel safely > redeploy approved artifact|Do not force-unlock or retry blindly while a deployment may still be active.
Quick revision|MR controls > pipeline rules > protected variables > artifact promotion|Protected branch, protected environment, and protected variables solve different risks."""),
    "docker": ("DOCKER", "#55c5ef", """Container request path|Ingress > published port > container network > process > dependency|Publish only required ports; binding to all host interfaces may expose a service.
Image lifecycle|Minimal base > pinned dependencies > build stages > signed image digest|Use a non-root runtime and avoid embedding secrets in image layers.
Isolation boundary|User namespace/capability drop > read-only root > seccomp > restricted network|Containers share a host kernel; treat the host and daemon as privileged boundaries.
Image delivery|Dockerfile > build/test/scan > registry push > digest-pinned deploy|Promote the image digest; tags such as `latest` are mutable.
Container observability|stdout/stderr > runtime logs > health probe > orchestrator signal|A Docker health check reports status but does not automatically restart every container.
Startup diagnosis|Image/config > entrypoint and exit code > mounted files > network/DNS|Inspect `docker logs`, `inspect`, and `exec` before rebuilding at random.
Data recovery|Named volume > backup consistency > restore test > application verification|Persist durable data outside the writable container layer.
Runtime resilience|Readiness/health > restart policy > resource limits > external dependency timeout|Restart loops can worsen outages; capture exit reason and fix startup cause.
Scenario: image is vulnerable|Identify deployed digest > rebuild patched base > scan and sign > roll out and verify|Know which running workloads still use the old digest.
Quick revision|Image is immutable template > container is process instance > volume persists data|Do not confuse a healthy container process with a healthy user journey."""),
    "kubernetes": ("KUBERNETES", "#69b6ff", """Pod request path|Ingress/Gateway > Service > ready EndpointSlice > Pod > dependency|A Service routes to ready endpoints; check selectors and readiness probes.
Workload lifecycle|Namespace/RBAC > Deployment > ReplicaSet > scheduled Pods|Use declarative manifests and wait for rollout status before declaring success.
Security boundary|OIDC user > RBAC role > service account > NetworkPolicy boundary|Default-deny networking only works when the CNI enforces NetworkPolicy.
Delivery path|Reviewed manifest > admission/policy > image digest > rollout and health|Pin image digests and separate deploy identity from runtime service account.
Cluster observability|Control plane/events > metrics/logs/traces > alert > owner runbook|Correlate namespace, workload, pod, and deployment revision.
Pod diagnosis|Events and status > scheduling/resources > probes > container logs|`CrashLoopBackOff` is a symptom; inspect previous-container logs and exit code.
Rollout recovery|Pause/rollback deployment > verify previous ReplicaSet > inspect traffic > resume|A rollback restores a revision; persistent schema/data changes may still need a forward fix.
Availability design|Replicas > topology spread > disruption budget > capacity headroom|A disruption budget cannot create spare nodes or guarantee zone capacity.
Scenario: rollout breaks service|Check endpoints and readiness > halt rollout > revert image/config > validate SLO|Keep probe thresholds aligned with actual startup and dependency behavior.
Quick revision|Deployment creates Pods > Service selects endpoints > ingress routes traffic|Check label selectors, namespace, policy, and readiness from outside inward."""),
    "jenkins": ("JENKINS", "#e7a859", """Pipeline path|SCM event > Jenkinsfile > isolated agent > test/build > artifact repository|Treat the Jenkins controller as a control plane; avoid running builds on it.
Pipeline lifecycle|Webhook > multibranch discovery > stage gates > deployment approval|Version the Jenkinsfile and make stages deterministic and restart-safe.
Credential boundary|Credential store > scoped binding > agent process > masked log and audit|Masking cannot prevent all exfiltration; never run untrusted code with deploy credentials.
Artifact delivery|Build once > test/scan > archive digest > promote approved artifact|Do not rebuild from a mutable branch for the production stage.
Controller signal|Queue/executor health > build failure trend > alerts > admin runbook|Monitor queue wait separately from build duration.
Build diagnosis|SCM checkout > agent label > toolchain > stage log > artifact result|Check agent capacity and environment before changing application code.
Credential incident|Disable credential > identify job scope > rotate downstream access > audit builds|Restrict credential domains and folder visibility.
Agent resilience|Ephemeral agents > bounded concurrency > workspace cleanup > controller backup|Back up configuration and credentials securely; test controller restoration.
Scenario: pipeline green, app unhealthy|Verify deployed artifact > target environment > rollout probe > rollback gate|Pipeline completion proves a job finished, not that users can use the service.
Quick revision|Controller orchestrates > agent executes > artifact is promoted|Keep plugins, controller, agents, and credentials within a patch/ownership plan."""),
    "terraform": ("TERRAFORM", "#a891ff", """Desired-state loop|Typed inputs > provider resources > plan diff > reviewed apply|State maps configuration addresses to remote objects; it is not a backup substitute.
Resource lifecycle|Write config > init/lock provider > validate/plan > apply and observe|Run plan against the intended workspace/backend before mutation.
Identity boundary|CI OIDC identity > cloud role > backend lock > provider API|Separate backend access from provider permissions and scope both narrowly.
Module delivery|Versioned module > pinned source/provider > test plan > promoted environment|Use stable inputs and interfaces; avoid hidden environment-specific behavior.
Operational signal|Plan drift > policy result > apply outcome > state/remote verification|A successful apply does not prove application-level health.
Plan diagnosis|Address and action > replacement attribute > dependency graph > state/backend check|Resolve unexpected replacement before apply; do not use `-target` as routine fix.
State recovery|Stop concurrent runs > secure state backup > inspect lineage/serial > restore/import|Never edit production state casually or share it through public artifacts.
Resilient identity|Remote encrypted state > lock/versioning > short-lived CI auth > tested restore|Protect state access as highly as cloud credentials.
Scenario: subnet key renamed|Review destroy/create addresses > add `moved` mapping if identity unchanged > plan|`for_each` keys are resource identity; a key change can replace real infrastructure.
Quick revision|`count` is positional > `for_each` is keyed > `plan` previews > `apply` changes|Use stable map keys for named resources; `sensitive` does not keep values out of state."""),
    "ansible": ("ANSIBLE", "#e7a859", """Automation path|Inventory and groups > playbook targeting > role/tasks > idempotent host state|Run against a controlled canary before expanding to the full fleet.
Change lifecycle|Review variables > syntax/lint check > check mode > staged rollout|Check mode is useful but not every module predicts all changes exactly.
Privilege boundary|Controller identity > SSH key/certificate > become rule > target audit|Limit sudo and protect controller credentials and inventory.
Configuration delivery|Versioned role > pinned collection > CI validation > tagged playbook run|Pin dependencies and record the exact revision used for each run.
Fleet signal|Play recap > failed/unreachable counts > callback log > ticket/runbook|Treat unreachable hosts separately from task failures.
Task diagnosis|Inventory match > connection facts > privilege escalation > module result|Use `-vv` selectively; ensure verbose output cannot reveal secrets.
Rollback recovery|Previous config artifact > targeted host group > restore task > service health|Prefer reversible templates and handler-driven service changes.
Resilient rollout|Serial batches > max failure threshold > health gate > continue/abort|Define abort criteria before a wide rollout begins.
Scenario: broken config pushed|Stop remaining batches > restore prior template > reload safely > verify service|Capture affected hosts and preserve the failed artifact for analysis.
Quick revision|Inventory selects hosts > playbook declares state > handlers restart on change|Idempotency means repeatable desired state, not automatically zero risk."""),
    "prometheus": ("PROMETHEUS", "#f36e75", """Metric path|Instrumented service > scrape target > time series > PromQL/recording rule|Use bounded labels; each unique label combination creates another series.
Monitoring lifecycle|Define SLI > expose metric > configure scrape > test query and alert|Validate target health, label names, and units before relying on an alert.
Access boundary|Scrape network > TLS/auth proxy > rule ownership > restricted UI/API|Prometheus is not an authorization system for every metric endpoint by default.
Alert delivery|Metric/rule > Prometheus alert > Alertmanager grouping > receiver/on-call|Test grouping, inhibition, and receiver delivery using a known alert.
Service signal|Request count/errors/latency > ratio and histogram > SLO burn > actionable page|Use histogram buckets consistently and avoid high-cardinality identifiers.
Target diagnosis|Service discovery > target labels > scrape error > endpoint/network|`up == 0` means scrape failed; it does not explain why.
Data recovery|Retention and disk > snapshot/backup > restore Prometheus > query verification|Local TSDB data is not a substitute for durable long-term storage.
Monitoring resilience|HA replicas > external labels > deduplicating receiver > tested notification|Two Prometheus servers can still share the same failure domain.
Scenario: alert storm|Group related alerts > suppress dependent symptoms > page on user impact > tune rule|Do not silence an alert without an owner and expiry.
Quick revision|Metrics measure numeric events > PromQL aggregates > alert routes notifications|Labels identify dimensions; never place user IDs or request IDs in metric labels."""),
    "grafana": ("GRAFANA", "#f3a35b", """Dashboard path|Data source > query and transformations > panel > dashboard viewer|A panel is only useful when units, time range, and labels are clear.
Dashboard lifecycle|Define audience/questions > select stable queries > version JSON > review and publish|Version dashboards as code and avoid undocumented UI-only production edits.
Access boundary|SSO team > folder permission > data-source credential > audit|A dashboard permission does not always constrain what a data source can query.
Alert delivery|Query condition > evaluation window > contact point > notification policy|Test routing, deduplication, and no-data behavior.
Operational signal|Golden signals > consistent variables > linked logs/traces > runbook|Use dashboard links that preserve service and time range context.
Panel diagnosis|Datasource health > query inspector > time range > labels/units|Check query latency and cardinality before raising dashboard refresh frequency.
Change recovery|Dashboard revision > compare diff > restore prior JSON > confirm permissions|Keep provisioning files and secrets separate.
Dashboard resilience|HA Grafana > durable database > external secret store > tested restore|A dashboard backup should include provisioning and critical configuration.
Scenario: alert did not page|Inspect rule evaluation > contact point test > policy match > receiver logs|Separate a rule that did not fire from a notification that did not route.
Quick revision|Panels answer questions > folders govern access > alerts route action|Dashboard availability is not the same as telemetry-source availability."""),
    "dynatrace": ("DYNATRACE", "#72d6bd", """Telemetry path|OneAgent/OpenTelemetry > entity model > service flow > problem detection|Validate coverage and entity attribution before tuning anomaly thresholds.
Onboarding lifecycle|Select pilot > deploy monitored agent > verify topology > expand by wave|Use a canary and document change windows and rollback steps.
Identity boundary|SSO group > environment role > management zone > audit event|Scope access to teams and entities; review inherited permissions.
Alert workflow|Problem event > Davis context > routing profile > owner and incident|Test the actual notification integration and deduplicate downstream.
Service signal|Service health > latency/error trend > dependency map > SLO action|Validate that monitored traffic represents real production paths.
Coverage diagnosis|Host process > agent status > network allowlist > tenant ingest|Check version compatibility, network egress, and licensing before redeploying.
Agent recovery|Identify faulty rollout > pause deployment > restore known-good version > verify data|Coordinate agent rollback with host and platform owners.
Observability resilience|Multiple ingest paths > tenant availability > alert fallback > export retention|Document what operators can see if the primary observability tenant is unavailable.
Scenario: noisy anomaly|Validate deployment context > inspect affected entities > tune scoped rule > watch recurrence|Avoid global threshold changes that hide unrelated failures.
Quick revision|Entities map dependencies > problems correlate evidence > ownership routes response|Instrumentation coverage and alert quality are separate workstreams."""),
    "splunk": ("SPLUNK", "#74c2ff", """Event path|Application/forwarder > input and sourcetype > index > SPL/search dashboard|Use a stable sourcetype contract and parse timestamps at ingestion.
Onboarding lifecycle|Define owner/fields > pilot input > validate events > scale collection|Estimate ingest volume and retention cost before enabling fleet-wide collection.
Access boundary|SSO role > index restriction > search capability > audit trail|Avoid broad index access and protect sensitive fields.
Alert workflow|SPL search > schedule/window > threshold > notable/on-call action|Choose a time window that matches ingestion delay and test alert suppression.
Data quality signal|Freshness > event count > parse errors > field extraction coverage|Alert on pipeline health, not just downstream search results.
Search diagnosis|Index/time range > sourcetype > timestamp > permissions/field extraction|Start with the narrowest index and time window; inspect raw events.
Ingest recovery|Stop bad input > preserve sample > repair parsing > replay/verify counts|Replay only with a deduplication and duplicate-event plan.
Search resilience|Indexer replication > forwarder buffering > queue monitoring > tested restore|Replication does not protect against every deletion or bad retention policy.
Scenario: license spike|Break down source volume > identify new input > throttle/fix > confirm ingest health|Do not drop security-critical events blindly to protect quota.
Quick revision|Index stores events > sourcetype shapes parsing > SPL filters and aggregates|Event-time correctness and field extraction affect every downstream search."""),
    "elk-stack": ("ELASTIC STACK", "#57c5b5", """Log path|Service event > shipper > Logstash/ingest pipeline > Elasticsearch > Kibana|Define timestamp, schema, and failure handling before onboarding volume.
Index lifecycle|Template and mapping > ingest pipeline > data stream > ILM rollover|Use explicit mappings for stable fields and test rollover/retention.
Access boundary|TLS identity > role/index privilege > field/document restriction > audit|Separate cluster administration from search and ingest identities.
Ingest delivery|Schema contract > pipeline test > staged source rollout > dashboard/alert|Monitor rejected documents and dead-letter flow during rollout.
Pipeline signal|Queue depth > ingest failures > shard health > disk watermark|Alert before disk exhaustion prevents writes.
Search diagnosis|Time range > index/data stream > mapping and query > shard/cluster health|A field mapped as text may require a keyword field for exact aggregation.
Disk recovery|Identify largest indices > check ILM/retention > free safe capacity > verify shards|Do not delete arbitrary indices without ownership and retention review.
Cluster resilience|Replica shards > zone allocation > snapshots > restore exercise|Replica copies are not backups against deletion or corruption.
Scenario: high disk watermark|Stop nonessential ingest > inspect shard/index growth > free approved space > confirm recovery|Avoid forced allocation changes before resolving disk and capacity.
Quick revision|Logstash transforms > Elasticsearch indexes > Kibana explores|Keep mappings, retention, and access rules intentional and versioned."""),
    "harness": ("HARNESS", "#e8ad50", """Delivery path|Service and environment > pipeline input > gated stage > deployment and health check|Model service, environment, and infrastructure ownership explicitly.
Pipeline lifecycle|Versioned pipeline > delegate/runner > approval policy > immutable artifact|Make manual approval visible and bind it to the artifact being promoted.
Identity boundary|Harness connector > scoped service account > secret manager > audit|Rotate connector credentials and grant only required deployment actions.
Release delivery|Build > scan and verify > artifact registry > environment promotion|Promote the same digest and retain deployment evidence.
Pipeline signal|Stage result > delegate health > deployment verification > owner notification|A completed stage needs an independent service health check.
Delegate diagnosis|Delegate connectivity > task permissions > secret access > execution logs|Distinguish delegate selection from target-system authorization.
Rollback path|Identify release > previous artifact/config > rollback stage > verify user path|Exercise rollback against the same deployment strategy as release.
Delivery resilience|Redundant delegates > bounded queue > retry policy > tested fallback|Avoid retries for non-idempotent deploy actions without a guard.
Scenario: stage succeeded, service degraded|Stop next stage > compare release and health > roll back > capture evidence|Gate later environments on observable health, not stage status alone.
Quick revision|Pipeline orchestrates > delegate executes > artifact is promoted|Keep approval, policy, and production credentials independently governed."""),
    "argo-cd": ("ARGO CD", "#ee7c6a", """GitOps path|Git commit > Argo CD comparison > sync policy > Kubernetes reconciliation|Git is desired state; check which revision Argo actually observed.
App lifecycle|Repository and path > Application target > sync > health and drift|Start manual sync in a sandbox; automate only after health checks are proven.
Identity boundary|Argo project > repo credentials > destination namespace > Kubernetes RBAC|Restrict project source repos, destinations, and resource kinds.
Promotion flow|Reviewed manifest > image digest update > environment repo > sync and verify|Promote a tested image digest rather than a mutable tag.
Sync signal|OutOfSync/Degraded > resource tree > app owner > runbook action|Alert on persistent health failure, not every transient reconciliation.
Sync diagnosis|Repo revision > render error > destination permissions > resource events|Check generated manifests and cluster events before repeating sync.
Rollback path|Known-good Git commit > revert desired-state change > reconcile > service check|A live kubectl patch will drift unless the desired Git state is corrected.
Controller resilience|HA controller > repo-server capacity > Redis/queue health > backup config|Protect repo credentials and test recovery of controller configuration.
Scenario: bad config auto-synced|Pause risky automation > revert commit > observe reconciliation > confirm SLO|Sync waves and health gates reduce blast radius but do not replace rollback plans.
Quick revision|Git declares > Argo compares > controller reconciles > health confirms|OutOfSync is difference; Degraded is health. They indicate different problems."""),
    "bash": ("BASH AUTOMATION", "#9bb8ff", """Script path|Validate arguments > check dependencies > run bounded command > report status|Use strict quoting and define expected failure behavior.
Script lifecycle|Write small function > shellcheck > test fixtures > staged schedule/run|Make scripts safe to rerun and provide a dry-run mode for destructive actions.
Privilege boundary|Dedicated account > narrow sudo command > validated input > audit output|Never interpolate untrusted input into `eval` or privileged shell strings.
Automation delivery|Versioned script > CI syntax/tests > signed package > controlled rollout|Pin external downloads and verify checksums/signatures.
Health signal|Exit code > structured log > duration > alert owner|Emit diagnostics to stderr and use stable exit codes for automation.
Failure diagnosis|Capture status > inspect stderr > check quoting/globbing > reproduce safely|Use `set -x` cautiously; traces can reveal secrets and expanded arguments.
Safe cleanup|Create explicit temp path > trap cleanup > check ownership > remove exact file|Never recursively remove a broad path or rely on an unchecked variable.
Run resilience|Timeout > bounded retries/backoff > lock > idempotent operation|A retry can duplicate side effects; use idempotency keys or detect prior work.
Scenario: partial failure|Stop on critical error > preserve logs > identify completed steps > resume safely|Design checkpoints so rerun does not corrupt already completed work.
Quick revision|Quote expansions > check command status > validate input > log outcome|Shell safety depends on context; `set -e` alone is not complete error handling."""),
    "python-devops": ("PYTHON FOR DEVOPS", "#62cfb2", """CLI path|Parse arguments > validate config > call API with timeout > structured result|Validate input before making a remote change.
Tool lifecycle|Define small functions > type and test > package > run in controlled identity|Separate pure transformations from side effects to make tests reliable.
Credential boundary|Workload identity > scoped API client > secret-safe logs > audit event|Do not hard-code tokens or log request headers and secret values.
Release flow|Lock dependencies > lint/unit tests > build wheel/container > deploy version|Use a reproducible dependency lock and promote a verified artifact.
Automation signal|Structured log > exit code > duration/retry count > runbook|Send logs to stderr when stdout is a machine-readable interface.
API diagnosis|Request ID > status and response class > timeout/retry policy > sanitized error|Retry only transient, idempotent operations; bound attempts and backoff.
Recovery path|Checkpoint > transaction/idempotency key > resume > reconcile final state|Persist enough state to avoid duplicate destructive side effects.
Runtime resilience|Timeouts > bounded concurrency > backoff/jitter > graceful shutdown|Limit concurrency to protect both caller and target API.
Scenario: API rate limited|Read retry-after > back off with jitter > resume safely > verify outcome|Do not turn a 429 into a tight retry loop.
Quick revision|Validate > timeout > retry safely > emit structured evidence|A correct exit code and actionable log are part of the CLI contract."""),
    "ai-agentic-devops": ("AI & AGENTIC DEVOPS", "#bd91ff", """Agent request path|Operator intent > policy and context > model proposal > tool gateway > reviewed action|Keep the model outside the trusted execution boundary.
Agent lifecycle|Define task boundary > curate context > simulate tools > staged release|Start read-only and measure before allowing any write action.
Tool security|Authenticated user > allowlisted tool > schema validation > approval for mutation|Prompt text is untrusted input; authorize tools independently of model output.
Change delivery|Model suggestion > policy/tests > human approval > normal CI deployment|Require the same review, tests, and audit as a human-authored change.
Agent telemetry|Tool invocation > actor and scope > approval/result > evaluation metric|Record inputs safely and minimize retention of sensitive prompts.
Failure diagnosis|Bad suggestion > retrieved context > tool result > policy/evaluation trace|Separate model error, stale context, tool failure, and authorization denial.
Incident containment|Disable write tools > revoke session tokens > preserve audit > restore normal workflow|Provide a tested kill switch outside the agent itself.
Agent resilience|Human fallback > bounded tools > rate limits > deterministic recovery path|Never make the agent the only way to restore a system it can modify.
Scenario: unsafe proposed change|Block tool call > explain policy denial > request human review > log evaluation|Measure unsafe-action prevention, not just task completion.
Quick revision|Model proposes > policy authorizes > tool executes > human owns outcome|Treat generated output as untrusted until validated and approved."""),
    "mlops": ("MLOPS", "#e39bda", """Model serving path|Versioned data > feature pipeline > model registry > serving endpoint > feedback|Track model, data, code, and serving configuration as one release lineage.
Experiment lifecycle|Define baseline > version data/code > train and evaluate > register candidate|Make experiments reproducible and compare against a meaningful baseline.
Model access boundary|Dataset identity > feature permissions > registry approval > serving identity|Restrict sensitive data and separate training from production-serving permissions.
Model delivery|Validation suite > bias/performance gate > signed model artifact > canary rollout|Promote the exact registered model artifact that passed validation.
Model health signal|Latency/errors > drift and quality > business outcome > retraining review|Drift is a signal to investigate, not an automatic justification to retrain.
Prediction diagnosis|Request features > preprocessing version > model signature > serving logs|Compare training and serving transformations for skew.
Model rollback|Current model/version > prior artifact > traffic shift > quality verification|Keep compatible feature schemas and a known-good serving configuration.
Serving resilience|Replicas > autoscaling > timeout/fallback > model-load readiness|Model startup and memory footprint must be included in capacity planning.
Scenario: quality drops after release|Check data and feature shift > compare cohort > roll back candidate > verify baseline|Use a predeclared quality threshold and owner before deployment.
Quick revision|Data lineage > reproducible training > gated registry > monitored inference|A model file without provenance and evaluation is not a production release."""),
    "selenium": ("SELENIUM TESTING", "#53c5a9", """Browser test path|Test intent > WebDriver session > browser action > assertion and report|Assert user-visible outcomes rather than implementation timing.
Test lifecycle|Arrange data > wait for condition > act > assert > clean up|Use explicit waits and independent test data to reduce flakiness.
Test identity boundary|Dedicated test account > least-privilege fixture > isolated environment > secret-safe report|Never reuse privileged production accounts in browser tests.
CI delivery|Pinned browser/driver > parallel test shard > report artifact > release gate|Keep browser, driver, and Selenium versions compatible and reproducible.
Test signal|Pass/fail and duration > screenshot/trace > flaky trend > owning team|Capture diagnostics on failure while redacting sensitive page content.
Failure diagnosis|Locator stability > wait condition > browser console > network/application log|Differentiate a stale locator, slow app, browser crash, and product defect.
Failure recovery|Preserve screenshot/log > quarantine with owner > fix root cause > restore gate|Do not permanently ignore flaky tests without an expiry and accountable owner.
Grid resilience|Remote WebDriver pool > session timeout > bounded queue > node health|Release browser sessions reliably, including after test failure.
Scenario: intermittent timeout|Compare run timeline > inspect app readiness > adjust condition > repeat on stable fixture|Avoid arbitrary sleeps; synchronize on a meaningful state.
Quick revision|Stable locator > explicit wait > isolated data > actionable report|A retry may hide a real race; track retry rate separately."""),
    "behavioural-system-design": ("BEHAVIOURAL & SYSTEM DESIGN", "#e6a35b", """Design path|Clarify users and scope > quantify load > define SLOs > draw components > test failure|State assumptions before selecting technologies.
Answer lifecycle|Situation/context > specific action > measurable result > reflection|Use first-person ownership and quantify outcomes without overclaiming.
Trust boundary|User/data classification > authentication > authorization > audit and retention|Include abuse cases and data lifecycle in the design, not as an appendix.
Architecture delivery|Requirements > API and schema > failure model > rollout/rollback plan|Explain migration and compatibility, not only the happy-path diagram.
Observability plan|User SLI > dependency metrics > traces/logs > alert and owner|Choose a measurable user outcome and explain how operators act on it.
Capacity diagnosis|Traffic shape > bottleneck > queue/backpressure > load-test evidence|Estimate orders of magnitude and state the assumptions.
Failure recovery|Detect > contain > restore from safe state > validate > learn|Prefer reversible mitigations before complex permanent fixes during an outage.
Resilience design|Redundancy > isolation > graceful degradation > game day|Name correlated failure risks; replicas alone do not guarantee resilience.
Scenario: major incident|Impact and timeline > decision/owner > customer communication > prevention|Be explicit about trade-offs, uncertainty, and when you would escalate.
Quick revision|Clarify > quantify > sketch > stress-test > summarize trade-offs|A good answer makes assumptions and failure behavior visible."""),
    "managerial-sre-interviews": ("MANAGERIAL & SRE", "#e5aa58", """Reliability path|Customer outcome > SLI/SLO > error budget > prioritization decision|Connect reliability work to an explicit user impact.
Incident leadership|Assign incident lead > establish facts > delegate work > communicate cadence|The lead coordinates; responders investigate with clear ownership.
Trust boundary|On-call access > least privilege > break-glass audit > post-incident review|Emergency access needs expiry and retrospective audit.
Change governance|Risk and SLO > progressive rollout > health gate > rollback threshold|Set rollback criteria before the change begins.
Operational signal|Burn rate > page policy > owner > learning review|Distinguish actionable pages from tickets and dashboards.
Diagnosis approach|Scope impact > validate hypothesis > test mitigation > observe outcome|State what evidence would disprove your hypothesis.
Recovery framework|Mitigate > restore service > validate data > follow up with prevention|Separate service restoration from root-cause analysis.
Team resilience|Reasonable on-call > runbooks > backup coverage > blameless learning|Blameless means accountable learning, not absence of ownership.
Scenario: repeated outage|Trend incidents > identify systemic risk > fund corrective work > measure recurrence|Propose a measurable follow-up owner and due date.
Quick revision|Impact > evidence > decision > communication > learning|Explain trade-offs clearly and invite missing constraints."""),
}

GUIDES = {
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "oci": "OCI",
    "linux": "Linux",
    "git": "Git",
    "github": "GitHub",
    "github-actions": "GitHub Actions",
    "gitlab": "GitLab",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "jenkins": "Jenkins",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "prometheus": "Prometheus",
    "grafana": "Grafana",
    "dynatrace": "Dynatrace",
    "splunk": "Splunk",
    "elk-stack": "ELK Stack",
    "harness": "Harness",
    "argo-cd": "Argo CD",
    "bash": "Bash",
    "python-devops": "Python for DevOps",
    "ai-agentic-devops": "AI and Agentic AI",
    "mlops": "MLOps",
    "selenium": "Selenium",
    "behavioural-system-design": "Behavioural and System Design",
    "managerial-sre-interviews": "Managerial and SRE Interviews",
}

WIDTH, HEIGHT = 1440, 900
BG, PANEL, INK, MUTED, LINE = "#0a1020", "#111b30", "#f3f6ff", "#aab8d0", "#293955"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def wrap(text: str, limit: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > limit and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def text(x: int, y: int, value: str, size: int, color: str, weight: int = 500) -> str:
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,Helvetica,sans-serif" '
            f'font-size="{size}" font-weight="{weight}">{esc(value)}</text>')


def multiline(x: int, y: int, value: str, size: int, color: str, limit: int, weight: int = 500) -> str:
    lines = wrap(value, limit)[:3]
    return "".join(
        f'<text x="{x}" y="{y + i * (size + 7)}" fill="{color}" '
        f'font-family="Arial,Helvetica,sans-serif" font-size="{size}" '
        f'font-weight="{weight}">{esc(line)}</text>'
        for i, line in enumerate(lines)
    )


def rect(x: int, y: int, w: int, h: int, fill: str, rx: int = 16, stroke: str = "none") -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'


def node(x: int, y: int, w: int, h: int, label: str, number: int, accent: str) -> str:
    return (
        rect(x, y, w, h, PANEL, 18, LINE)
        + f'<circle cx="{x + 30}" cy="{y + 31}" r="15" fill="{accent}" fill-opacity=".18"/>'
        + text(x + 25, y + 37, str(number), 15, accent, 700)
        + multiline(x + 58, y + 28, label, 19, INK, 19, 650)
    )


def arrow(x1: int, y1: int, x2: int, y2: int, accent: str) -> str:
    return (
        f'<path d="M{x1} {y1} C{(x1+x2)//2} {y1}, {(x1+x2)//2} {y2}, {x2} {y2}" '
        f'fill="none" stroke="{accent}" stroke-width="3" stroke-opacity=".8" marker-end="url(#arrow)"/>'
    )


def diagram(nodes: list[str], index: int, accent: str) -> str:
    out = []
    if index == 5:
        out.append(node(520, 342, 400, 92, nodes[0], 1, accent))
        out.append(arrow(720, 434, 445, 490, accent))
        out.append(arrow(720, 434, 995, 490, accent))
        out.append(node(245, 494, 400, 92, nodes[1], 2, accent))
        out.append(node(795, 494, 400, 92, nodes[2], 3, accent))
        out.append(arrow(445, 586, 720, 612, accent))
        out.append(arrow(995, 586, 720, 612, accent))
        out.append(node(520, 620, 400, 92, nodes[3], 4, accent))
        out.append(text(260, 477, "CHECK", 13, accent, 700))
        out.append(text(1010, 477, "COMPARE", 13, accent, 700))
    elif index == 6:
        for i, label in enumerate(nodes):
            y = 330 + i * 96
            out.append(f'<circle cx="176" cy="{y+36}" r="21" fill="{accent}" fill-opacity=".18"/>')
            out.append(text(169, y + 42, str(i + 1), 16, accent, 700))
            out.append(rect(220, y, 955, 74, PANEL, 16, LINE))
            out.append(multiline(250, y + 31, label, 20, INK, 77, 600))
            if i < len(nodes) - 1:
                out.append(f'<path d="M176 {y+59} V{y+96}" stroke="{accent}" stroke-width="3"/>')
    elif index == 7:
        out.append(node(520, 342, 400, 92, nodes[0], 1, accent))
        out.append(node(255, 494, 390, 92, nodes[1], 2, accent))
        out.append(node(795, 494, 390, 92, nodes[2], 3, accent))
        out.append(node(520, 620, 400, 86, nodes[3], 4, accent))
        out.append(arrow(575, 434, 450, 494, accent))
        out.append(arrow(865, 434, 990, 494, accent))
        out.append(arrow(450, 586, 575, 620, accent))
        out.append(arrow(990, 586, 865, 620, accent))
        out.append(text(310, 477, "PRIMARY", 13, accent, 700))
        out.append(text(1034, 477, "FALLBACK", 13, accent, 700))
    elif index == 9:
        positions = [(210, 350), (750, 350), (210, 510), (750, 510)]
        for i, (x, y) in enumerate(positions):
            out.append(rect(x, y, 480, 126, PANEL, 18, LINE))
            out.append(f'<circle cx="{x+35}" cy="{y+35}" r="16" fill="{accent}" fill-opacity=".2"/>')
            out.append(text(x + 30, y + 41, str(i+1), 15, accent, 700))
            out.append(multiline(x + 68, y + 36, nodes[i], 19, INK, 30, 650))
    else:
        xs = [118, 430, 742, 1054]
        for i, label in enumerate(nodes):
            out.append(node(xs[i], 364, 268, 114, label, i + 1, accent))
            if i < 3:
                out.append(arrow(xs[i] + 268, 421, xs[i + 1] - 10, 421, accent))
        if index == 2:
            out.insert(0, f'<rect x="716" y="340" width="622" height="190" rx="22" fill="none" stroke="{accent}" stroke-dasharray="9 9" stroke-width="2" stroke-opacity=".65"/>')
            out.append(text(746, 332, "TRUSTED / CONTROLLED ZONE", 13, accent, 700))
        if index == 4:
            for i, (x, label) in enumerate(zip(xs, nodes)):
                out.append(f'<circle cx="{x+16}" cy="338" r="5" fill="{accent}"/>')
                out.append(text(x, 522, ("SCOPE", "TREND", "THRESHOLD", "ACTION")[i], 13, accent, 700))
    return "".join(out)


def render_svg(guide: str, acronym: str, accent: str, index: int, title: str,
               nodes: list[str], check: str) -> str:
    archetype, caption = ARCHETYPES[index]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<defs><linearGradient id="wash" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{accent}" stop-opacity=".17"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{accent}"/></marker></defs>
{rect(0, 0, WIDTH, HEIGHT, BG, 0)}
<circle cx="1340" cy="95" r="220" fill="url(#wash)"/>
<path d="M64 146H1376" stroke="{LINE}" stroke-width="2"/>
{rect(64, 48, 52, 52, accent, 15)}
{text(76, 82, acronym[:3].upper(), 17, BG, 800)}
{text(132, 70, guide.upper(), 15, accent, 750)}
{text(132, 99, "FIELD GUIDE  /  VISUAL SERIES", 12, MUTED, 600)}
{rect(1196, 51, 180, 42, PANEL, 20, LINE)}
{text(1220, 78, f"{index+1:02d}  /  10", 15, INK, 700)}
{text(68, 205, archetype, 14, accent, 750)}
{multiline(68, 250, title, 38, INK, 49, 750)}
{multiline(68, 298, caption, 18, MUTED, 105, 500)}
{diagram(nodes, index, accent)}
{rect(64, 730, 1312, 106, PANEL, 20, LINE)}
{rect(86, 754, 7, 56, accent, 4)}
{text(116, 773, "PRODUCTION CHECK", 13, accent, 750)}
{multiline(116, 805, check, 18, INK, 122, 550)}
{text(68, 872, "DEVSECOPS STUDY NOTES   •   ORIGINAL LEARNING GRAPHIC", 12, MUTED, 600)}
{text(1160, 872, esc(guide), 12, MUTED, 600)}
</svg>'''


def create_guide(folder: str, name: str, acronym: str, color: str, rows: str) -> list[str]:
    entries = [row.split("|") for row in rows.strip().splitlines()]
    if len(entries) != 10 or any(len(row) != 3 for row in entries):
        raise ValueError(f"{folder}: expected exactly ten title|steps|check rows")
    target = NOTES / folder / "visuals"
    target.mkdir(parents=True, exist_ok=True)
    readme = ["# Visual study cards", "", f"Ten original visuals for the [{name} guide](../README.md). "
              "Open the SVG for a crisp, scalable version; use PNG for slides and quick viewing.", ""]
    for i, (title, path, check) in enumerate(entries):
        steps = [step.strip() for step in path.split(">")]
        if len(steps) > 4:
            steps = steps[:3] + [" / ".join(steps[3:])]
        while len(steps) < 4:
            steps.append("Verify outcome")
        slug = "-".join("".join(char.lower() if char.isalnum() else "-" for char in title).split())
        slug = "-".join(filter(None, slug.split("-")))[:48]
        stem = f"{i+1:02d}-{slug}"
        svg_path, png_path = target / f"{stem}.svg", target / f"{stem}.png"
        svg_path.write_text(render_svg(name, acronym, color, i, title, steps, check), encoding="utf-8")
        subprocess.run(
            ["sips", "-s", "format", "png", str(svg_path), "--out", str(png_path)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        with Image.open(png_path) as source:
            source.convert("RGB").quantize(
                colors=256, method=Image.Quantize.FASTOCTREE
            ).save(png_path, format="PNG", optimize=True, compress_level=9)
        readme.extend([
            f"## {i+1:02d}. {title}", "",
            f"![{name}: {title}]({stem}.png)", "",
            f"[SVG source]({stem}.svg) · [PNG image]({stem}.png)", "",
        ])
    (target / "README.md").write_text("\n".join(readme).rstrip() + "\n", encoding="utf-8")
    product_readme = NOTES / folder / "README.md"
    content = product_readme.read_text(encoding="utf-8")
    marker = "## Visual study cards"
    if marker not in content:
        content = content.rstrip() + (
            f"\n\n{marker}\n\n"
            f"Browse the [10 original visual study cards](visuals/README.md) "
            "as SVG or PNG, covering architecture, workflow, security, delivery, "
            "observability, troubleshooting, recovery, resilience, scenarios, and revision.\n"
        )
        product_readme.write_text(content, encoding="utf-8")
    return [f"[{name}](../{folder}/visuals/README.md)"]


def main() -> None:
    for folder, name in GUIDES.items():
        guide, color, rows = DATA[folder]
        create_guide(folder, name, guide, color, rows)
    index = [
        "# Visual guide library", "",
        "The 28 product guides each include ten original, topic-specific study cards in SVG and PNG. "
        "Cards cover a system map, workflow, security, delivery, observability, diagnosis, recovery, "
        "resilience, a production scenario, and rapid revision. The visuals are newly authored and "
        "do not reproduce the inaccessible LinkedIn reference image.", "",
        "Regenerate the cards on macOS with Python 3 and Pillow installed: "
        "`python3 notes/visuals/generate.py`. The script uses `sips` for SVG rendering.", "",
    ]
    for folder, name in GUIDES.items():
        index.append(f"- [{name}](../{folder}/visuals/README.md)")
    (NOTES / "visuals" / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    main_readme = NOTES / "README.md"
    content = main_readme.read_text(encoding="utf-8")
    marker = "## Visual guide library"
    if marker not in content:
        content = content.rstrip() + (
            "\n\n## Visual guide library\n\n"
            "Explore [10 original SVG/PNG study cards for each of the 28 guides](visuals/README.md).\n"
        )
        main_readme.write_text(content, encoding="utf-8")
    print(f"Generated {len(GUIDES)} guides × 10 cards in SVG and PNG.")


if __name__ == "__main__":
    main()
