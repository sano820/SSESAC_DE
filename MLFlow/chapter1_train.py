import mlflow
from mlflow.models import infer_signature 
import pandas as pd 
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X,y = datasets.load_iris(return_X_y=True)

X_train, X_test, y_train, y_test= train_test_split(
    X,y,test_size=0.2, random_state=42
)

params = {
    'solver' : 'lbfgs', #logistic regression 알고리즘 
    'max_iter' : 1000, 
    'multi_class' : 'auto', #분류 
    'random_state' : 8888
}

lr = LogisticRegression(**params) 
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

mlflow.set_tracking_uri(uri='http://127.0.0.1:5000')
mlflow.set_experiment('QuickStart')

with mlflow.start_run() : 
    mlflow.log_params(params)
    mlflow.log_metrics({'accuracy':accuracy})
    mlflow.set_tag('Training info','Basic LR model for Iris Data')

    signature = infer_signature(X_train, lr.predict(X_train)) # y_train은 실제값, 예측력을 알기위해 predict함수 사용 

    model_info = mlflow.sklearn.log_model( # 사이킷런 데이터를 사용하기에 sklearn 모델로 지원) 
        sk_model = lr,                     # 로깅할때는 각 프레임워크마다 다르게 지정 
        name = 'iris_model',      # 이따 불러올때는 일반화된 방법으로 가져옴 
        signature = signature,             # 데이터 구조가 조금씩 다르기 때문에 각기 다른 함수를 지원 
        input_example = X_train,           # 파라미터가 다르기 때문에 함수를 프레임워크에 따라 지원 
        registered_model_name = 'tracking-quickstart'
    )
