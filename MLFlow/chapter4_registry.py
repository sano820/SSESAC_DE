import mlflow
import pandas as pd

loaded_model = mlflow.pyfunc.load_model(f'models:/model-signature-quickstart@baseline')
# model_uri:model:/(등록된 모델이름)@(alias이름)

example_data = pd.DataFrame([
    {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
    {"sepal_length": 6.2, "sepal_width": 2.8, "petal_length": 4.8, "petal_width": 1.8},
    {"sepal_length": 5.9, "sepal_width": 3.0, "petal_length": 5.1, "petal_width": 1.8}
])

predictions = loaded_model.predict(example_data)
print(predictions)