import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 불러오기 및 확인
file_path = './0719 dominance.csv'
df = pd.read_csv(file_path)
print(df.head())
print(df.info())

# 데이터 컬럼명 확인 및 필요시 변환
df.columns = [col.strip() for col in df.columns]
print(df.columns)

# 2. 인클로져별 도미넌스 추이 분석
plt.figure(figsize=(12, 6))
sns.lineplot(x='Age', y='Dominance', hue='Enclosure', data=df)
plt.title('인클로져별 도미넌스 추이')
plt.xlabel('Age')
plt.ylabel('Dominance')
plt.legend(title='Enclosure')
plt.show()

# 3. 시간에 따른 도미넌스 변화 분석
plt.figure(figsize=(12, 6))
sns.lineplot(x='Time', y='Dominance', hue='Enclosure', data=df)
plt.title('시간에 따른 도미넌스 변화')
plt.xlabel('Time')
plt.ylabel('Dominance')
plt.legend(title='Enclosure')
plt.show()

# 4. 도미넌스와 체중 간의 관계 분석
plt.figure(figsize=(12, 6))
sns.scatterplot(x='BodyWeight', y='Dominance', hue='Enclosure', data=df)
plt.title('도미넌스와 체중 간의 관계')
plt.xlabel('BodyWeight')
plt.ylabel('Dominance')
plt.legend(title='Enclosure')
plt.show()
