# SRE and managerial interview scenario process

## 1. Clarify the scenario

Ask who is affected, scope/regions, duration, data integrity/safety, SLO, dependencies, current release/change, and available responders. State assumptions rather than silently inventing facts.

## 2. Stabilize and lead

Declare severity; name incident commander, operations lead, and communications owner. Freeze risky changes; prioritize user safety and reversible mitigation. Set update cadence and decision log. Do not wait for root cause before containing impact.

## 3. Diagnose with signals

Compare healthy and affected slices; examine user SLIs, golden signals, dependency traces, saturation, deploy markers, quota, and audit events. Form testable hypotheses and make one controlled change at a time.

## 4. Verify recovery

Confirm user-facing success/error/latency, data consistency, queue drain, and no recurrence through an agreed observation window. If uncertain, communicate uncertainty and maintain mitigation.

## 5. Review and improve

Conduct a blameless review of contributing conditions, detection, response, and recovery. Create prioritized actions with owner, due date, and measurable verification; track completion and reassess residual risk.

## 6. Answer managerial questions

For prioritization, state impact/urgency/risk/dependencies and what is deferred. For conflict, explain listening, evidence, decision, communication, and outcome. For feedback/performance, be specific, timely, fair, supportive, and clear about expectations/follow-up.

## Interview self-check

Did I ask about user impact? Separate mitigation from root-cause analysis? State SLO/risk trade-offs? Communicate ownership and cadence? Verify outcome? Describe learning without blame?
