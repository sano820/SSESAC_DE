# app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="자동 데이터 분석 대시보드", layout="wide")

st.title("📊 자동 데이터 분석 대시보드")
st.markdown("""
사용자가 업로드한 CSV 데이터를 분석하고, 선택한 변수와 모델로 학습 후 결과를 시각화합니다.
""")

# ------------------------
# 1️⃣ CSV 업로드
# ------------------------
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())
    
    # 숫자 컬럼 추출
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    # ------------------------
    # 2️⃣ 변수 선택
    # ------------------------
    st.subheader("변수 선택")
    y_col = st.selectbox("종속변수(Y) 선택", options=numeric_cols)
    x_cols = st.multiselect("독립변수(X) 선택", options=[c for c in numeric_cols if c != y_col])

    if y_col and x_cols:
        X = df[x_cols]
        y = df[y_col]
        
        # ------------------------
        # 3️⃣ 모델 선택
        # ------------------------
        st.subheader("모델 선택")
        model_option = st.radio("모델 선택", ("Linear Regression", "Decision Tree", "Random Forest"))

        if model_option == "Linear Regression":
            model = LinearRegression()
        elif model_option == "Decision Tree":
            model = DecisionTreeRegressor()
        else:
            n_estimators = st.slider("Random Forest 트리 개수", 10, 200, 100)
            model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        
        # ------------------------
        # 4️⃣ 모델 학습
        # ------------------------
        test_size = st.slider("테스트 데이터 비율", 0.1, 0.5, 0.2)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # ------------------------
        # 5️⃣ 성능 평가
        # ------------------------
        st.subheader("모델 성능 평가")
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        st.write(f"RMSE: {rmse:.3f}")
        st.write(f"R²: {r2:.3f}")
        
        # ------------------------
        # 6️⃣ 시각화
        # ------------------------
        st.subheader("예측 vs 실제 시각화")
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.scatterplot(x=y_test, y=y_pred, ax=ax)
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel("Y_test")
        ax.set_ylabel("Y_pred")
        st.pyplot(fig)
        
        if model_option in ["Decision Tree", "Random Forest"]:
            st.subheader("변수 중요도")
            importances = model.feature_importances_
            imp_df = pd.DataFrame({"feature": x_cols, "importance": importances}).sort_values(by="importance", ascending=False)
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            sns.barplot(x="importance", y="feature", data=imp_df, ax=ax2)
            st.pyplot(fig2)
        
        # ------------------------
        # 7️⃣ 예측값 다운로드
        # ------------------------
        st.subheader("예측 결과 다운로드")
        result_df = X_test.copy()
        result_df["y_true"] = y_test
        result_df["y_pred"] = y_pred
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name="predictions.csv", mime="text/csv")

