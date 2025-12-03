# 📊 자동 데이터 분석 대시보드 (Streamlit)

사용자가 업로드한 CSV 데이터를 기반으로, 변수 선택과 모델 학습을 클릭 몇 번으로 수행하고 결과를 시각화까지 보여주는 **자동 데이터 분석 대시보드** 프로젝트입니다.  

---

## 🚀 기능
1. **CSV 파일 업로드**
   - 사용자가 CSV 파일을 업로드하면 데이터를 자동으로 읽어와 확인 가능
2. **변수 선택**
   - 종속변수(Y)와 독립변수(X)를 선택
   - 숫자 컬럼 자동 필터링
3. **모델 선택**
   - Linear Regression
   - Decision Tree Regressor
   - Random Forest Regressor (트리 개수 설정 가능)
4. **모델 학습 및 평가**
   - 학습/테스트 데이터 분할
   - 성능 평가 지표 제공: RMSE, R²
5. **시각화**
   - 실제값 vs 예측값 scatter plot
   - Decision Tree / Random Forest의 경우 변수 중요도 bar plot
6. **예측 결과 다운로드**
   - 예측값과 실제값을 CSV로 다운로드 가능

---

## 🛠 설치 방법
```
# 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 필요 패키지 설치
pip install streamlit pandas numpy scikit-learn matplotlib seaborn
```

## 🏃 실행 방법
```
streamlit run app.py
```
1. 웹 브라우저가 자동으로 열리며 대시보드 접속
2. CSV 업로드 → 변수 선택 → 모델 선택 → 분석/시각화 확인
3. 필요 시 예측 결과 CSV 다운로드