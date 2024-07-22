import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 불러오기 및 확인
file_path = './0719 dominance.csv'
df = pd.read_csv(file_path)
print(df.head())
print(df.info())

# 2. 인클로저별 도미넌스 추이 분석
# 필요한 컬럼만 선택
dominance_cols = ['Age', 'enclosure', 'location-pink', 'location-orange', 'location-green', 'location-black', 'location-purple', 'location-navy']
dominance_df = df[dominance_cols].dropna()

# 데이터 변환: 위치 컬럼을 녹여서 long-form으로 변환
dominance_df = pd.melt(dominance_df, id_vars=['Age', 'enclosure'], var_name='Location', value_name='Rank')

# 인클로져별 도미넌스 추이 분석
plt.figure(figsize=(12, 6))
sns.lineplot(x='Age', y='Rank', hue='enclosure', data=dominance_df)
plt.title('인클로져별 도미넌스 추이')
plt.xlabel('Age')
plt.ylabel('Rank')
plt.legend(title='Enclosure')
plt.show()

# 3.시간에 따른 도미넌스 차이 분석
# 시간 컬럼의 결측값 제거
time_df = df[['Time', 'enclosure'] + [col for col in df.columns if col.startswith('location-')]].dropna()

# 데이터 변환: 위치 컬럼을 녹여서 long-form으로 변환
time_df = pd.melt(time_df, id_vars=['Time', 'enclosure'], var_name='Location', value_name='Rank')

# 시간에 따른 도미넌스 변화 분석
plt.figure(figsize=(12, 6))
sns.lineplot(x='Time', y='Rank', hue='enclosure', data=time_df)
plt.title('시간에 따른 도미넌스 변화')
plt.xlabel('Time')
plt.ylabel('Rank')
plt.legend(title='Enclosure')
plt.show()


# 4. 도미넌스와 체중 간의 관계분석
# 필요한 컬럼만 선택
weight_df = df[['BodyWeight', 'enclosure'] + [col for col in df.columns if col.startswith('location-')]].dropna()

# 데이터 변환: 위치 컬럼을 녹여서 long-form으로 변환
weight_df = pd.melt(weight_df, id_vars=['BodyWeight', 'enclosure'], var_name='Location', value_name='Rank')

# 도미넌스와 체중 간의 관계 분석
plt.figure(figsize=(12, 6))
sns.scatterplot(x='BodyWeight', y='Rank', hue='enclosure', data=weight_df)
plt.title('도미넌스와 체중 간의 관계')
plt.xlabel('BodyWeight')
plt.ylabel('Rank')
plt.legend(title='Enclosure')
plt.show()
