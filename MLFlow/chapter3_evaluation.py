import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load dataset
X,y = load_iris(return_X_y=True)
iris_feature_names = load_iris().feature_names

# Convert to DataFrame
df = pd.DataFrame(X, columns= iris_feature_names)
df['target'] = y 


train, test = train_test_split(
    df, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=200)
model.fit(train[iris_feature_names], train['target'])

model_uri = "model_logistic_regression"
mlflow.sklearn.save_model(model, model_uri)

eval_result = mlflow.evaluate(
    model = model_uri,
    data = test,
    targets = 'target',
    model_type = 'classifier',
)

print(eval_result.metrics)