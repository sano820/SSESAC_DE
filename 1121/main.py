import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 데이터 로드
df = pd.read_csv("./1120/data/insurance.csv")

# 0. 간단한 EDA (구조 파악 및 결측치 탐색)
print(df.shape)
print(df.head())
print(df.info())

# 1. X, y 분리 (drop을 활용하세요!)
X = df.drop("charges", axis=1)
y = df["charges"]

# 스케일링할 컬럼 이름 목록을 리스트를 정의하세요
num_cols = ['age','bmi', 'children']
# 인코딩할 컬럼 이름 목록을 리스트로 정의하세요
cat_cols = ['sex','smoker','region']

# 2. 원핫 인코딩
# 인코더 생성하기
ohe = OneHotEncoder()
# 인코딩할 컬럼만 따로 추출하세요
X_categories = X[cat_cols]
# 원핫 인코딩 수행하기
X_cat_encoded = ohe.fit_transform(X_categories).toarray()

# 3. 스케일링(Z-Score)
# 스케일러 생성하기
scaler = StandardScaler()
# 스케일링할 컬럼만 따로 추출하세요
X_nums = X[num_cols]
# 스케일링 수행하기
X_num_scaled = scaler.fit_transform(X_nums)

# [수정 금지] 인코딩한 결과와 스케일링한 결과 합치기
# X_final: 스케일링/인코딩을 수행한 최종 결과 데이터
X_final = np.concatenate([X_num_scaled, X_cat_encoded], axis=1)

# 4. 훈련, 테스트 데이터 분할 (8:2)
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# 5. 회귀 모델 생성 후, 훈련
model = LinearRegression()
model.fit(X_train, y_train)

# 6. 예측 진행
pred = model.predict(X_test)

# 실제 값과 예측 값 비교하는 데이터프레임 생성
result = pd.DataFrame({
    'y_actual' : y_test,
    'y_predicted' : pred
})
print(result)

# 7. 평가 진행 및 결과 출력
# -실제 값과 예측 값과의 오차에 대한 평가
rmse = np.sqrt(mean_squared_error(y_test, pred))
print("RMSE:", rmse) # RMSE
print(r2_score(y_test, pred)) # R2 Score