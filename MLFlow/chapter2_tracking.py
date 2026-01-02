import os
import mlflow
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split

mlflow.set_tracking_uri(uri = 'http://127.0.0.1:5000')
experiment = mlflow.set_experiment('new_experiment')

# Load the Iris dataset
X, y = datasets.load_iris(return_X_y=True)

# Split the data into training and test_sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Convert to DataFrame
X_train_df = pd.DataFrame(X_train, columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
X_test_df = pd.DataFrame(X_test,columns= ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])

y_train_df = pd.DataFrame(y_train, columns=['target'])
y_test_df = pd.DataFrame(y_test, columns=['target'])

# Save to CSV
os.makedirs("my_artifacts", exist_ok=True)
X_train_df.to_csv("my_artifacts/X_train.csv", index=False)
X_test_df.to_csv("my_artifacts/X_test.csv", index=False)
y_train_df.to_csv("my_artifacts/y_train.csv", index=False)
y_test_df.to_csv("my_artifacts/y_test.csv", index=False)   


# Start and MLFlow run
with mlflow.start_run() : 
    # Logging single paragmeters
    mlflow.log_param('learning_rate', 0.01)
    mlflow.log_param('batch_size', 32)
    mlflow.log_param('num_epochs', 10)

    # my_artifacts_ex1 디렉토리에 있는 파일들을 experiment_logs로
    mlflow.log_artifacts("my_artifacts", artifact_path="experiment_logs")

    mlflow.set_tag('experiment_type','Baseline')
    mlflow.set_tag("author", 'codemake')
    mlflow.set_tag("framework", 'sklearn')

    tags = {
        'dataset':'iris',
        'version':'1.0'
    }
    mlflow.set_tags(tags)

    # logging multiple parameters
    params = {"optimizer":"adam", "dropout":0.2, "activation":"relu"}
    mlflow.log_params(params)

    # logging metrics at different steps
    for epoch in range(10):
        loss = np.exp(-epoch /2) # simulating decreasing loss
        accuracy = epoch / 10.0 # simulating increasing accuaracy

        mlflow.log_metric('loss', loss, step=epoch)
        mlflow.log_metric('accuracy', accuracy, step=epoch)

    final_metrics = {'final_loss' : loss, 'final_accuracy' : accuracy}
    mlflow.log_metrics(final_metrics, step=10)

print("Experiment logged, run 'mlflow ui' to visualize results")