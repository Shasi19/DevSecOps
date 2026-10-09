"""Small, reproducible MLflow experiment example; not a production trainer."""

import os

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def main() -> None:
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "file:./mlruns"))
    mlflow.set_experiment("devsecops-iris-example")

    data = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        data.data,
        data.target,
        test_size=0.2,
        random_state=42,
        stratify=data.target,
    )
    model = LogisticRegression(max_iter=500, random_state=42)

    with mlflow.start_run():
        mlflow.log_param("model", "LogisticRegression")
        mlflow.log_param("max_iter", 500)
        mlflow.log_param("random_state", 42)
        model.fit(x_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(x_test))
        mlflow.log_metric("holdout_accuracy", accuracy)
        mlflow.sklearn.log_model(model, artifact_path="model")
        print(f"holdout_accuracy={accuracy:.4f}")


if __name__ == "__main__":
    main()
