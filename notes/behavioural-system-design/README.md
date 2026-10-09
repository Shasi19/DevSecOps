# Behavioural and system-design interviews

## Behavioural answers

Use a structured story: **Situation** (brief context), **Task** (your responsibility), **Action** (specific choices and collaboration), and **Result** (measurable outcome and learning). Be precise about your contribution; distinguish what you led from what the team did. Prepare examples for conflict, failure, ambiguity, prioritization, ownership, mentoring, and customer impact. A strong failure story explains the signal missed, corrective action, and changed practice without blaming others.

## System-design approach

1. Clarify functional requirements, users, scale, latency, availability, consistency, and constraints.
2. Estimate orders of magnitude (requests, storage, bandwidth) and state assumptions.
3. Draw a simple end-to-end architecture: clients, APIs, compute, data, queues, and dependencies.
4. Define data model and API contracts; explain consistency and idempotency.
5. Walk through bottlenecks and failure modes; add caching/partitioning only when justified.
6. Cover security, observability, deployment, capacity, and disaster recovery.
7. Identify trade-offs and summarize what you would validate next.

Explain a baseline before optimizing. For each component, name its failure mode, detection signal, and mitigation. Be explicit when a requirement is unclear instead of silently inventing one.

## Practice

Design a webhook delivery service. Discuss signature verification, durable queues, retries/backoff, duplicate delivery, per-tenant limits, dead-letter handling, and delivery observability. Then tell a STAR story about a production incident you helped resolve.

## Interview checklist

Keep answers structured, state assumptions, invite correction, and leave time for trade-offs and follow-up questions. Do not claim ownership of work you did not perform.
