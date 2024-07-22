import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import seaborn as sns


# 데이터 불러오기 및 컬럼명 정리
file_path = './0719 dominance_modify.csv'
df = pd.read_csv(file_path)

# 컬럼명 정리
df.columns = [
    'order', 'RoomTemp', 'Humidity', 'Age', 'Enclosure', 'Time', 
    'location-pink', 'location-orange', 'location-green', 'location-black', 
    'location-purple', 'location-navy', 'sum', 'Carton-pink', 
    'Carton-orange', 'Carton-green', 'Carton-black', 'Carton-purple', 
    'Carton-navy', 'Unnamed: 19', 'Unnamed: 20'
]

# Age 컬럼의 결측값을 제거한 후 int 형식으로 변환
df = df.dropna(subset=['Age'])
df['Age'] = df['Age'].astype(int)

# Time 컬럼을 시:분 형식으로 변환하여 문자열로 저장
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce').dt.strftime('%H:%M')

def plot_dominance_ranking(enclosure_df, ax, title):
    """지배력 순위 그래프를 그리는 함수"""
    # 모든 날짜에 대해 데이터 필터링
    ages = enclosure_df['Age'].unique()

    # 데이터를 long-form으로 변환
    age_long = pd.melt(enclosure_df, id_vars=['Age', 'Time'], value_vars=[
        'location-pink', 'location-orange', 'location-green', 
        'location-black', 'location-purple', 'location-navy'],
        var_name='Location', value_name='Rank')

    # Rank를 1등이 맨 위로, 6등이 아래로 오도록 반전
    age_long['Rank'] = 7 - age_long['Rank']

    # Age와 Time을 결합하여 새로운 x축 값 생성
    age_long['AgeTime'] = age_long['Age'].astype(str) + '-' + age_long['Time']

    # 새로운 x축 값을 숫자로 변환
    age_long['AgeTime_num'] = pd.factorize(age_long['AgeTime'])[0]

    # Location별로 데이터를 나누어 시각화
    for location in age_long['Location'].unique():
        location_data = age_long[age_long['Location'] == location]
        # 보간을 위한 함수 생성
        f = interp1d(location_data['AgeTime_num'], location_data['Rank'], kind='cubic')
        age_time_new = np.linspace(location_data['AgeTime_num'].min(), location_data['AgeTime_num'].max(), num=100, endpoint=True)
        rank_smooth = f(age_time_new)
        ax.plot(age_time_new, rank_smooth, label=location.split('-')[1])
        # 실제 데이터 포인트에 점과 레이블 추가
        ax.scatter(location_data['AgeTime_num'], location_data['Rank'])
        for i in range(len(location_data)):
            ax.text(location_data['AgeTime_num'].iloc[i], location_data['Rank'].iloc[i], f"{location_data['Rank'].iloc[i]:.1f}",
                    horizontalalignment='center', verticalalignment='bottom')

    # 실제 데이터의 x축 레이블 생성
    unique_agetimes = age_long[['AgeTime_num', 'AgeTime']].drop_duplicates().sort_values('AgeTime_num')
    unique_agetimes['Time'] = unique_agetimes['AgeTime'].apply(lambda x: x.split('-')[1])
    ax.set_xticks(unique_agetimes['AgeTime_num'])
    ax.set_xticklabels(unique_agetimes['Time'], rotation=60, ha='right')

    # Age 구간 표시
    for age in ages:
        age_start = unique_agetimes[unique_agetimes['AgeTime'].str.startswith(str(age))]['AgeTime_num'].min()
        age_end = unique_agetimes[unique_agetimes['AgeTime'].str.startswith(str(age))]['AgeTime_num'].max()
        ax.axvline(x=age_end, color='grey', linestyle='--')
        ax.text((age_start + age_end) / 2, ax.get_ylim()[0] - 0.5, f'Age {age}', horizontalalignment='center', verticalalignment='center', fontsize=12, bbox=dict(facecolor='white', edgecolor='none'))

    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Rank (1st on top)')
    ax.invert_yaxis()  # Y축 반전
    ax.legend(title='Location')
    ax.grid(True)

# Enclosure 1부터 5까지의 데이터 필터링
enclosures = [1.0, 2.0, 3.0, 4.0, 5.0]
fig, axes = plt.subplots(5, 1, figsize=(20, 30))

for i, enclosure in enumerate(enclosures):
    enclosure_df = df[df['Enclosure'] == enclosure]
    plot_dominance_ranking(enclosure_df, axes[i], f'Enclosure {int(enclosure)} Dominance Ranking Over Time')

plt.tight_layout()
plt.show()


# 3

# 데이터 불러오기 및 컬럼명 정리
file_path = './0719 dominance_modify.csv'
df = pd.read_csv(file_path)

# 컬럼명 정리
df.columns = [
    'order', 'RoomTemp', 'Humidity', 'Age', 'Enclosure', 'Time', 
    'location-pink', 'location-orange', 'location-green', 'location-black', 
    'location-purple', 'location-navy', 'sum', 'Carton-pink', 
    'Carton-orange', 'Carton-green', 'Carton-black', 'Carton-purple', 
    'Carton-navy', 'Unnamed: 19', 'Unnamed: 20'
]

# Age 컬럼의 결측값을 제거한 후 int 형식으로 변환
df = df.dropna(subset=['Age'])
df['Age'] = df['Age'].astype(int)

def plot_median_rank_with_confidence_intervals(enclosure_df, ax, title):
    """중앙값 및 신뢰 구간 그래프를 그리는 함수"""
    # 데이터를 long-form으로 변환
    long_df = pd.melt(enclosure_df, id_vars=['Age', 'Time'], value_vars=[
        'location-pink', 'location-orange', 'location-green', 
        'location-black', 'location-purple', 'location-navy'],
        var_name='Location', value_name='Rank')

    # Age별, Location별 Rank의 중앙값, 표준편차 계산
    agg_df = long_df.groupby(['Age', 'Location'])['Rank'].agg(
        median='median', 
        std='std'
    ).reset_index()

    # 신뢰 구간 계산 (95% 신뢰 구간)
    agg_df['ci95_hi'] = agg_df['median'] + 1.96 * (agg_df['std'] / np.sqrt(len(agg_df)))
    agg_df['ci95_lo'] = agg_df['median'] - 1.96 * (agg_df['std'] / np.sqrt(len(agg_df)))

    sns.lineplot(x='Age', y='median', hue='Location', data=agg_df, marker='o', palette='tab10', ax=ax)

    # 각 점에 대해 신뢰 구간을 구간으로 표시
    for loc in agg_df['Location'].unique():
        loc_data = agg_df[agg_df['Location'] == loc]
        ax.fill_between(loc_data['Age'], loc_data['ci95_lo'], loc_data['ci95_hi'], alpha=0.2)
        for i in range(len(loc_data)):
            y = loc_data['median'].iloc[i]
            label = f"{loc.split('-')[1]}:{loc_data['median'].iloc[i]:.1f}"
            
            # Median 값이 0.5 내외로 차이가 나는 경우 텍스트 위치 조정
            if i > 0 and abs(y - loc_data['median'].iloc[i - 1]) < 0.5:
                ax.text(loc_data['Age'].iloc[i], y + 0.1, label, horizontalalignment='center', verticalalignment='bottom')
            else:
                ax.text(loc_data['Age'].iloc[i], y - 0.1, label, horizontalalignment='center', verticalalignment='top')

    # Rank가 작은 값이 위로 가도록 설정
    ax.invert_yaxis()

    ax.set_title(title)
    ax.set_xlabel('Age')
    ax.set_ylabel('Median Rank')
    ax.legend(title='Location')
    ax.grid(True)

# Enclosure 1부터 5까지의 데이터 필터링
enclosures = [1.0, 2.0, 3.0, 5.0, 6.0]
fig, axes = plt.subplots(5, 1, figsize=(14, 40))

for i, enclosure in enumerate(enclosures):
    enclosure_df = df[df['Enclosure'] == enclosure]
    plot_median_rank_with_confidence_intervals(enclosure_df, axes[i], f'Enclosure {int(enclosure)} Median Rank Over Age')

plt.tight_layout()
plt.show()
