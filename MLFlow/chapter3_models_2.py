import mlflow
import pandas as pd


# 모델이 로깅된 경로 명시
logged_model ='runs:/29b9eb8c9fd6421d82a44ad36b40cf87/iris_model'

# pyfunc으로 모델 불러오기
loaded_model = mlflow.pyfunc.load_model(logged_model)

# 예시 입력 데이터 (모델 입력 스키마에 유효한)
example_data = pd.DataFrame([
    {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
    {"sepal_length": 6.2, "sepal_width": 2.8, "petal_length": 4.8, "petal_width": 1.8},
    {"sepal_length": 5.9, "sepal_width": 3.0, "petal_length": 5.1, "petal_width": 1.8}
])

predictions = loaded_model.predict(example_data)

example_data["predicted_class"] = predictions
print(example_data)


# # 예시 입력 데이터( 모델 입력 스키마에 유효하지 않은)
# incorrect_example_data = pd.DataFrame([
#     {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4},
#     {"sepal_length": 6.2, "sepal_width": 2.8, "petal_width": 1.8},
#     {"sepal_width": 3.0, "petal_length": 5.1, "petal_width": 1.8}
# ])


# predictions = loaded_model.predict(incorrect_example_data)

# incorrect_example_data["predicted_class"] = predictions
# print(incorrect_example_data)