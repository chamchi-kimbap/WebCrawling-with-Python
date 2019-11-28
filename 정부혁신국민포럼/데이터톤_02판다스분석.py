#%% import
%reset -f
import os
os.getcwd()
from os import chdir
os.chdir('C:\\Users\\UOS\\Documents\\GITHUB\\WebCrawling-with-Python')
pdir = os.getcwd() ;print(pdir)

import pandas as pd
import seaborn as sns # 시각화
import matplotlib.pyplot as plt
# 그래프의 스타일을 지정
plt.style.use('ggplot')
import matplotlib as mpl
mpl.rcParams.update({'font.size':14})
plt.rc('font',family='Malgun Gothic') # windows
%matplotlib inline 

#%% 데이터
df = pd.read_csv("정부혁신국민포럼/suggestion.csv", encoding='utf-8-sig')
df.shape
df.head()

#df = df.drop(['Unnamed: 0'],1)
df.drop(df.columns[[0]], axis=1, inplace=True) # 색인으로제거

df.info()
df.describe(include='all')  # int data 요약
df['category'].value_counts()

figure, (ax1, ax2) = plt.subplots(1,2)
figure.set_size_inches(20,10)
sns.countplot(data=df, y="category", ax=ax1)
sns.barplot(data=df, x="vote", y="category", ax=ax2) # 평균 투표수? & 신뢰구간 검은선

df_category = pd.DataFrame(df.groupby(['category'])['vote'].sum()) \
                            .reset_index().sort_values('vote',ascending=False) # 각 카테고리별로 vote를 sum
df_category.head()

#%% 기간 as.Date
df['start'] = pd.to_datetime(df['start']) 
df['end'] = pd.to_datetime(df['end'])
df.dtypes
df['start-date'] = df['start'].dt.date # dt를 이용해 요일을 가져올수 있게 한다
df['start-month'] = df['start'].dt.year.astype(str) + "-" + df['start'].dt.month.astype(str)
df['start-weekday'] = df['start'].dt.dayofweek
df['start-day'] = df['start'].dt.day
df[['start-date','start-month','start-weekday']].head()

weekday_map = {0:'월', 1:'화', 2:'수', 3:'목', 4:'금', 5:'토', 6:'일'}
df['weekday'] = df['start-weekday'].apply(lambda x : weekday_map[x])

#%% 그림그리기
#plt.figure(figsize=(20,5))
plt.title('일별 제안 수')
plt.xticks(rotation=60, ha='right')
sns.countplot(data=df.sort_values(by="start-date", ascending=True), x="start-day")
#plt.title('월별 제안 수')
#sns.countplot(data=df.sort_values(by="start-date", ascending=True), x="start-month")

plt.title('일별 투표 수 (날짜는 제안일 기준)')
sns.pointplot(data=df.sort_values(by="start-date", ascending=True), x="start-day", y="vote") # 평균을 그려준다. estimate default = mean

plt.title('일별 투표 수 (날짜는 제안일 기준)')
sns.barplot(data=df.sort_values(by="start-date", ascending=True), x="start-day", y="vote")
# 편차가 크다 : 일부 제안이 다른 제안에 비해 많은 투표를 받음

plt.title('요일별 제안 수')
sns.countplot(data=df.sort_values(by="start-weekday", ascending=True), x="weekday") 

plt.title('요일별 투표 수(제안일 기준)')
sns.barplot(data=df.sort_values(by="start-weekday", ascending=True), x="weekday", y="vote") 

#%%
df_06_10 = df[df['start'] > '2019-06-10'] # 6월 10일 이후
df_06_10['start-date'].value_counts()

df.loc[df["vote"]>=10, ["sgId", "start", "title", "category", "content"]] # 투표수가 10건 이상인 것 보고싶다.

#%%
pd.set_option('display.max_columns', 500)

#%%
df
