# 설치하기
# !pip install matplotlib
# matplotlib 불러오기
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

year = [2018, 2019, 2020, 2021, 2022, 2023]
python = [5.8, 8.17, 9.31, 11.87, 15.63, 14.51]
C = [13.59, 14.08, 16.72, 14.32, 12.71, 14.73]
java = [15.78, 15.04, 16.73, 11.23, 10.82, 13.23]
JS = [3.49, 2.51, 2.38, 2.44, 2.12, 2.1]

'''
plt.subplots() 함수를 이용해 1행 3열로 총 세개의 서브플롯을 생성합니다. (레이아웃 조정 옵션 추가)
생성된 서브플롯은 변수 ax1, ax2, ax3에 저장합니다.

서브플롯 ax1
파이썬의 연도별 점유율을 선 그래프로 그립니다.
제목: "파이썬의 점유율"
x축 라벨: "연도"
y축 라벨: "점유율"

서브플롯 ax2
자바의 연도별 점유율을 선 그래프로 그립니다.
제목: "자바의 점유율"
x축 라벨: "연도"

서브 플롯 ax3
C언어의 연도별 점유율을 선 그래프로 그립니다.
제목: "C언어의 점유율"
x축 라벨: "연도"
'''

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12,5), constrained_layout=True)

ax1.plot(year, python, marker='o', color='b', label='Python')
ax1.set_title('파이썬의 점유율')
ax1.set_xlabel('연도')
ax1.set_ylabel('점유율')

ax2.plot(year, java, marker='o', color='r', label='Java')
ax2.set_title('자바의 점유율')
ax2.set_xlabel('연도')

ax3.plot(year, C, marker='o', color='g', label='C')
ax3.set_title('C언어의 점유율')
ax3.set_xlabel('연도')

plt.show()