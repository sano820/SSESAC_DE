# Manual Specification 방식 Example

import mlflow
from mlflow.models import ModelSignature
from mlflow.types.schema import Schema, ColSpec

import os
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X,y = datasets.load_iris(return_X_y=True)
iris_feature_names = datasets.load_iris().feature_names

X_train, X_test, y_train, y_test = train_test_split(
    X,y, test_size=0.2, random_state=42
)

params ={
    'solver':'lbfgs',
    'max_iter':1000,
    "multi_class":"auto",
    "random_state":8888,
}

lr = LogisticRegression(**params)
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

mlflow.set_tracking_uri(uri='http://127.0.0.1:5000')
mlflow.set_experiment("MLFow Model Signature")

input_schema = Schema([
    ColSpec("double", name="sepal_length"),
    ColSpec("double", name="sepal_width"),
    ColSpec("double", name="petal_length"),
    ColSpec("double", name="petal_width")
])
output_schema = Schema([ColSpec('long')])

signature = ModelSignature(inputs=input_schema, outputs = output_schema)

with mlflow.start_run():
    mlflow.log_params(params)
    mlflow.log_metric('accuracy', float(accuracy))
    mlflow.set_tag("Training_info", "Basic LR model for iris data")

    model_info = mlflow.sklearn.log_model(
        sk_model = lr,
        artifact_path = 'iris_model',
        signature= signature, 
        input_example = pd.DataFrame(X_train, columns = iris_feature_names),
        registered_model_name = "model-signature-quickstart", # 모델 등록
    )

    # load the model back for predictions as a genric python Funtion model
    loaded_model = mlflow.pyfunc.load_model(model_info.model_uri)
    X_test_df = pd.DataFrame(X_test, columns=['sepal_length','sepal_width','petal_length','petal_width'])
    predictions = loaded_model.predict(X_test_df)

    # Store results in a DataFrame
    result = pd.DataFrame(X_test, columns=iris_feature_names)
    result['actual_class'] = y_test
    result['predicted_class'] = predictions

    print(result[:4])