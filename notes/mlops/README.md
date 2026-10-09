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
