import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('1120/data/seoul_park.csv')

# 2018년 4월 데이터 필터링
df_2018_apr = df[(df['연'] == 2018) & (df['월'] == 4)]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
#-----
# matplotlib으로 박스 플롯 그리기
#-----  
# ax1.boxplot(df_2018_apr['어린이'])
ax1.boxplot([df_2018_apr['어린이'], df_2018_apr['청소년'], df_2018_apr['어른']], labels=['어린이', '청소년', '어른'])
ax1.set_xticklabels(['어린이', '청소년', '어른'])
ax1.set_ylabel('어린이')
ax1.set_title('2018년 4월 어린이 박스 플롯 (matplotlib)')

# --------------
# seaborn으로 박스 플롯 그리기
# --------------
# sns.boxplot(data=df_2018_apr, y ='어린이', ax=ax2)

# seaborn 박스플롯을 위한 long-form 변환
# melt 함수는 wide-form 데이터를 long-form 데이터로 변환
df_melt = df_2018_apr[['어린이', '청소년', '어른']].melt(
    var_name='구분', value_name='값'
)
# seaborn 박스플롯
sns.boxplot(data=df_melt, x='구분', y='값', ax=ax2)

ax2.set_title('2018년 4월 어린이 박스 플롯 (seaborn)')
plt.show()  