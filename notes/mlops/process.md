# MLOps model-to-production process

## 1. Define model and data contract

State intended use, target population, label definition, exclusions, acceptable error/fairness thresholds, privacy/licensing constraints, latency/cost limits, and human fallback. Version schema and validate freshness, nulls, ranges, duplicates, leakage, distribution, and label quality.

## 2. Make training reproducible

Record source commit, dataset/feature snapshot, transformation code, parameters, dependency/container digest, random seeds, hardware, and metrics. Split data to avoid leakage (time/group split when appropriate). Track experiments; keep a test set isolated from iterative tuning.

## 3. Evaluate and register

Compare against a baseline on holdout and relevant slices. Evaluate calibration, robustness, fairness, privacy/security, latency, and resource use. Set promotion gates and independent approval. Register immutable model artifact with lineage, model card, known limitations, and rollback version. Aggregate score alone does not imply production fitness.

## 4. Deploy progressively

Select batch/online/streaming based on freshness and latency. Validate feature parity between training and serving. Shadow then canary a version; route a small controlled cohort. Keep schema backward-compatible and preserve immediate traffic/model rollback. Retraining creates a candidate; it does not automatically authorize production.

## 5. Monitor

Monitor service uptime/latency/errors/cost plus feature freshness, schema violations, training-serving skew, input/prediction drift, delayed-label quality, fairness slices, and business outcomes. Define thresholds, owners, and response. Drift is an investigation signal, not proof of degradation.

## 6. Respond to regression

Check telemetry/data pipeline first; compare cohorts, features, model version, and recent changes. If impact crosses policy, switch to known-good model or deterministic fallback. Preserve lineage consistent with privacy rules; evaluate a candidate offline before promotion.

## 7. Retire model and data

Stop traffic, revoke serving identity, remove endpoint/scaling resources, archive required model cards/evaluations, apply data retention/deletion policy, and remove stale feature jobs. Verify downstream consumers no longer depend on retired model.
