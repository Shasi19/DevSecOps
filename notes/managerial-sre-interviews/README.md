# Managerial and SRE interviews

## SRE foundations

Reliability is a user-visible property. Define SLIs (measures), SLOs (targets over a window), and—where useful—SLAs (external commitments). An error budget represents tolerated unreliability; use it to make explicit decisions about release risk and reliability work. Avoid treating 100% availability as a default target because it is costly and often unnecessary.

Discuss incident response as a system: detection, severity, clear incident command, communication, mitigation, recovery, and a blameless learning review. Prioritize safe mitigation before root-cause certainty. Follow-ups should have owners and measurable outcomes. Capacity planning, automation, toil reduction, change management, and disaster recovery are ongoing responsibilities.

## Managerial scenarios

For prioritization, state impact, urgency, dependencies, risk, and what will be deferred. For conflict, surface goals and evidence, listen, decide transparently, and revisit outcomes. For performance or team health, use timely specific feedback, clear expectations, support, and follow-through. Explain how you balance delivery, reliability, security, and people sustainability.

## Scenario response pattern

Clarify impact and scope; identify immediate safety/containment actions; assign roles and communication; use telemetry to form hypotheses; make reversible changes first; verify recovery against user-facing indicators; then review contributing factors and prevention.

## Practice

Respond to a regional dependency outage during a release. Explain whether to halt the rollout, how to protect users, what data informs the decision, who communicates, and how to restore service. Then define the post-incident actions and how success will be measured.

## Further reading

[Google SRE books](https://sre.google/books/) · [Incident management guide](https://sre.google/workbook/incident-response/)
