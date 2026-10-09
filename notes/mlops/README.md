# MLOps

## Mental model

MLOps applies software delivery and operational discipline to machine-learning systems. The lifecycle includes data collection, validation, feature processing, training, evaluation, registration, deployment, monitoring, and retirement. Model behavior depends on code, data, features, configuration, and runtime—not weights alone.

## Reproducible workflow

Version code and capture data lineage, feature definitions, parameters, environment, and evaluation results for each run. Validate data schema, quality, and distribution before training. Track experiments and register only models that pass agreed evaluation and governance checks. Promote a specific model artifact with provenance; never retrain implicitly during deployment. Use a model registry and reproducible pipelines.

## Deployment and monitoring

Choose batch, online, streaming, or edge serving based on latency, throughput, cost, and freshness. Shadow/canary deployment can compare a candidate safely. Monitor service availability/latency and model-specific indicators: input drift, prediction distribution, quality when labels arrive, fairness constraints, and business outcomes. Data drift is not automatically model failure, but it should trigger investigation. Define rollback and retraining criteria explicitly.

## Security and governance

Protect training data and model artifacts, control access, and audit lineage. Assess privacy, bias, explainability, licensing, and adversarial risks. Validate that models cannot leak sensitive training information beyond policy. Ensure automated retraining cannot promote an unreviewed or poisoned artifact.

## Practice

Build a small training pipeline with schema checks, experiment tracking, a model registry, an offline evaluation gate, and a canary deployment. Simulate feature drift and document the alert, decision, and rollback.

## Further reading

[MLflow documentation](https://mlflow.org/docs/latest/) · [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)

## Topic roadmap and ML delivery architecture

**Lifecycle topics:** data contracts/validation, feature engineering/store, experiment tracking, training orchestration, evaluation, model registry, packaging, serving, monitoring, retraining, governance, and retirement. Track code, data/version, features, parameters, environment, model artifact, evaluation, and approval together.

```mermaid
flowchart LR
  DATA[Versioned data] --> VALID[Validation]
  VALID --> TRAIN[Training + experiment tracking]
  TRAIN --> EVAL[Evaluation / fairness gates]
  EVAL --> REG[Model registry]
  REG --> DEP[Batch or online serving]
  DEP --> MON[Latency + quality + drift]
  MON --> REVIEW[Human / policy review]
  REVIEW --> TRAIN
```

**Example:** register only a candidate that passes a reproducible offline evaluation and data-quality checks. Deploy by immutable model version to shadow/canary, compare business and safety metrics, then promote or roll back. Retraining should create a candidate, not automatically authorize production.

**Monitoring:** input schema/null/range checks, training-serving skew, feature freshness, prediction distribution, delayed-label quality, fairness slices, latency/error/cost, and drift. Drift is a signal to investigate—not proof of model degradation.

**Troubleshooting:** training result irreproducible—missing data/code/environment version; serving mismatch—feature transformation skew; accuracy drop—label delay, cohort shift, pipeline bug or concept drift; model unavailable—artifact permissions, runtime compatibility, capacity and health checks.

**Revision:** model != full ML system; registry records candidates; data lineage matters; offline quality != online impact; monitor both system and model; rollback to known model; re-training must be governed and evaluated.

## Reproducible experiment lab

See [`examples/train.py`](examples/train.py) for a small MLflow-tracked classification experiment. It demonstrates deterministic split, metrics, parameters, and artifact logging only. It is not a production training pipeline: add versioned input data, schema/quality checks, dependency lock, model card, fairness/security evaluation, registry approval, and deployment/monitoring gates before reuse.

## End-to-end MLOps process

See [`process.md`](process.md) for data contract/versioning, experiment creation, evaluation gates, model registration, deployment/canary, monitoring, rollback, and retraining approval.
