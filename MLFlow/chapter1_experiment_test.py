# mlflow tracking
import mlflow

mlflow.set_tracking_uri(uri='http://127.0.0.1:5000')

exp = mlflow.set_experiment('new_experiment')

print(f'ID: {exp.experiment_id}')
print(f'Name: {exp.name}')
print(f'Artifact Locatijon: {exp.artifact_location}')
print(f'LifeCycle Stage: {exp.lifecycle_stage}')

for i in range(3) : 
    with mlflow.start_run() :         
        mlflow.log_text("hello", "test.txt")
        mlflow.log_param('iteration', i)
        mlflow.log_metric('accuracy', 0.8 + i * 0.05)

        with open('example.txt', 'w') as f :
            f.write('This is an example artifact')
        mlflow.log_artifact('MLFflow/example_test.txt')

# 3번 Run을 돌리는데,
# 각 Run 마다 parm, metric, artifact를 logging하는 것 
# new_experiment라는 그룹 안에 종속되어있는 Run들 