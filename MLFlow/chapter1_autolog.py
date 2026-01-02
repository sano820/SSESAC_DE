import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

mlflow.set_tracking_uri(uri = "http://127.0.0.1:5000")
mlflow.set_experiment('MLFlow QuickStart')

# 입력 데이터셋 샘플을 볼수 있는 옵션
mlflow.autolog(log_input_examples= True)

iris = load_iris()
X_train, X_test, y_train,y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

with mlflow.start_run():
    model= RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42)
    model.fit(X_train,y_train)
    mlflow.sklearn.log_model(model, 'random_forest_model')