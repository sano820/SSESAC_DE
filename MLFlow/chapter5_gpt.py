import mlflow
import mlflow.sklearn
import numpy as np

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, log_loss, confusion_matrix
)

def eval_and_log(y_true, y_pred, y_proba=None):
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
    }
    if y_proba is not None:
        metrics["roc_auc"] = roc_auc_score(y_true, y_proba)
        metrics["log_loss"] = log_loss(y_true, y_proba)
    mlflow.log_metrics(metrics)

    # confusion matrix artifact (간단히 텍스트로)
    cm = confusion_matrix(y_true, y_pred)
    mlflow.log_text(str(cm), "confusion_matrix.txt")


def main():
    # 1) 데이터
    data = load_breast_cancer()
    X, y = data.data, data.target

    # 2) split (stratify + seed 고정)
    seed = 42
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y
    )

    # 3) MLflow 실험
    mlflow.set_experiment("breast_cancer_compare")

    # 4) 모델 정의 (전처리 포함)
    models = {
        "logreg": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000, random_state=seed))
        ]),
        "random_forest": RandomForestClassifier(
            n_estimators=300, random_state=seed
        ),
        "knn": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", KNeighborsClassifier(n_neighbors=7))
        ]),
    }

    # 공통 파라미터
    common_params = {
        "dataset": "sklearn_breast_cancer",
        "test_size": 0.2,
        "seed": seed,
    }

    # 5) 모델별 run
    for name, model in models.items():
        with mlflow.start_run(run_name=name):
            mlflow.set_tag("model_name", name)
            mlflow.log_params(common_params)

            # 모델별 파라미터도 기록(가능한 범위)
            mlflow.log_param("model_class", model.__class__.__name__)

            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            y_proba = None
            if hasattr(model, "predict_proba"):
                y_proba = model.predict_proba(X_test)[:, 1]

            eval_and_log(y_test, y_pred, y_proba)

            # 모델 저장
            mlflow.sklearn.log_model(model, artifact_path="model")

if __name__ == "__main__":
    main()
