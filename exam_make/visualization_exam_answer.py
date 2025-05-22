'''
# 어떤 인코딩을 해야하는지 확인
import chardet

# human.csv 파일 인코딩 확인
with open('human.csv', 'rb') as f:
    result = chardet.detect(f.read())
    print(result['encoding'])
'''

'''
import pandas as pd

df = pd.read_csv('human.csv', encoding='EUC-KR')
df.info()
# print(df)
# print(df.columns)


human_df = pd.DataFrame()
human_df['city'] = df['시도명']
human_df['country'] = df['시군구명']
human_df['male'] = df['남자']
human_df['female'] = df['여자']
human_df['20s_male'] = df[['20세남자', '21세남자', '22세남자', '23세남자', '24세남자',
                               '25세남자', '26세남자', '27세남자', '28세남자', '29세남자']].apply(pd.to_numeric).sum(axis=1)

human_df['20s_female'] = df[['20세여자', '21세여자', '22세여자', '23세여자', '24세여자',
                               '25세여자', '26세여자', '27세여자', '28세여자', '29세여자']].apply(pd.to_numeric).sum(axis=1)
human_df['30s_male'] = df[['30세남자', '31세남자', '32세남자', '33세남자', '34세남자',
                               '35세남자', '36세남자', '37세남자', '38세남자', '39세남자']].apply(pd.to_numeric).sum(axis=1)

human_df['30s_female'] = df[['30세여자', '31세여자', '32세여자', '33세여자', '34세여자',
                               '35세여자', '36세여자', '37세여자', '38세여자', '39세여자']].apply(pd.to_numeric).sum(axis=1)



human_df = human_df[human_df['city'] == '서울특별시']

# print(human_df)

# 서울특별시 인구 통계 자료
human_df.to_csv('human_data.csv', encoding='UTF8')
'''

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

human_df = pd.read_csv('human_data.csv', encoding='UTF8')
# human_df.info()

# 1. 구별 인구수 분석
population_by_country = human_df.groupby('country')[['male','female']].sum().stack().reset_index()
population_by_country.columns = ['country', 'sex', 'population']

# 결과 확인
print('\n1. 구별 인구수 분석')
print(population_by_country)
# print(population_by_country.columns)

# 한글 폰트 깨짐 해결 코드
plt.rcParams['font.family']='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


# 시각화 : 막대그래프
plt.figure(figsize=(10,6)) # 그래프 크기 설정
# seaborn을 사용하여 막대 그래프 생성
sns.barplot(data=population_by_country, x='country', y='population', hue='sex')
plt.title('analysis of population numbers by country') # 그래프 제목
plt.xlabel('country') # x축 레이블
plt.ylabel('population') # y축 레이블
plt.xticks(fontsize=7)
plt.yticks(fontsize=7)

# 그래프 레이아웃 조정
plt.tight_layout()
# 그래프 표시
plt.show()


# 2. 구별 20대와 30대의 인구수 분석
human_df['20s'] = human_df['20s_male'] + human_df['20s_female']
human_df['30s'] = human_df['30s_male'] + human_df['30s_female']

# print(human_df)

population_by_age = human_df.groupby('country').agg(
    {'20s' : 'sum',
     '30s' : 'sum'
     }).reset_index()

print(population_by_age)

# 시각화 : 누적 그래프 그리기
population_by_age.plot(kind='bar', stacked=True, x='country', figsize=(10,6))
plt.title('Analysis of the population by age and country') # 제목 설정
plt.xlabel('country')  # x축 레이블
plt.ylabel('Age')  # y축 레이블
plt.xticks(rotation=45,fontsize=7)
plt.yticks(fontsize=7)
plt.tight_layout()
plt.show()

# 두개의 그래프 한 하면에 출력
# 대시보드 생성
fig = plt.figure(figsize=(10, 8))

ax1 = plt.subplot(2, 1, 1)
sns.barplot(data=population_by_country, x='country', y='population', hue='sex', palette='Set2', ax=ax1)
ax1.set_title('구별 성별 인구 분석')
ax1.set_ylabel('인구 수')
ax1.tick_params(axis='x', rotation=45, labelsize=6)

ax2 = plt.subplot(2, 1, 2)
population_by_age.plot(kind='bar', stacked=True, x='country', ax=ax2)
ax2.set_title('구별 20대 및 30대 인구 분석')
ax2.set_ylabel('인구 수')
ax2.tick_params(axis='x', rotation=45, labelsize=6)

plt.suptitle('서울특별시 인구 통계 대시보드', fontsize=12)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()