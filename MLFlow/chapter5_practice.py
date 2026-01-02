# train_compare.py
import os
from pathlib import Path

import mlflow
import mlflow.sklearn

import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix


# mlflow 설정
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("breast_cancer_compare")

# 데이터 로드
X, y = load_breast_cancer(return_X_y=True)

# Train/Test split
seed = 42
test_size = 0.2
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=test_size,
    stratify=y,
    random_state=seed
)

# 공통 파라미터
common_params = {
    "dataset": "sklearn_breast_cancer",
    "seed": seed,
    "test_size": test_size,
}

# 모델 정의
models = {
    "logreg": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(C=1.0, max_iter=2000, random_state=seed))
    ]),
    "knn": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", KNeighborsClassifier(n_neighbors=7))
    ]),
    "random_forest": Pipeline([
        ("clf", RandomForestClassifier(n_estimators=300, max_depth=None, random_state=seed))
    ]),
}

# confusion matrix 이미지 저장할 임시 폴더
artifact_dir = Path("artifacts_tmp")
artifact_dir.mkdir(exist_ok=True)

# 모델별 run
for name, model in models.items():
    with mlflow.start_run(run_name=name):
        # -------------------------
        # 파라미터 기록
        # -------------------------
        mlflow.log_params(common_params)
        mlflow.log_param("model_name", name)

        # 모델별 핵심 파라미터만 추가 기록
        params = model.get_params()
        print(params)

        if name == "logreg":
            mlflow.log_param("C", params["clf__C"])
            mlflow.log_param("max_iter", params["clf__max_iter"])
            mlflow.log_param("scaler", "StandardScaler")
        elif name == "knn":
            mlflow.log_param("n_neighbors", params["clf__n_neighbors"])
            mlflow.log_param("scaler", "StandardScaler")
        elif name == "random_forest":
            mlflow.log_param("n_estimators", params["clf__n_estimators"])
            mlflow.log_param("max_depth", params["clf__max_depth"])
            mlflow.log_param("scaler", "None")

        # -------------------------
        # 학습 & 예측
        # -------------------------
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # -------------------------
        # 메트릭 기록(precision/recall/accuracy)
        # -------------------------
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)



        # -------------------------
        # confusion matrix 이미지 저장 + log_artifact
        # 지피티가 작성해줌!
        # -------------------------
        cm = confusion_matrix(y_test, y_pred)

        fig = plt.figure()
        plt.imshow(cm)  # 기본 스타일 그대로(색 지정 안함)
        plt.title(f"Confusion Matrix - {name}")
        plt.xlabel("Predicted")
        plt.ylabel("True")
        plt.xticks([0, 1], ["0", "1"])
        plt.yticks([0, 1], ["0", "1"])

        # 값 표시
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, str(cm[i, j]), ha="center", va="center")

        plt.tight_layout()

        cm_path = artifact_dir / f"confusion_matrix_{name}.png"
        fig.savefig(cm_path, dpi=150)
        plt.close(fig)

        mlflow.log_artifact(str(cm_path))

        # -------------------------
        # 모델 아티팩트 기록(log_model)
        # -------------------------
        mlflow.sklearn.log_model(model, artifact_path="model")
