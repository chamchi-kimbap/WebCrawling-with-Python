###################################################
######### 정부혁신국민포럼 페이지 크롤링 ##########
###################################################

# https://www.innogov.go.kr/ucms/ogp/sug/list.do?menuNo=300011
# 저작권 확인 robots.txt
# https://www.innogov.go.kr/robots.txt

#%% import
%reset -f
import os
os.getcwd()
from os import chdir
os.chdir('C:\\Users\\UOS\\Documents\\GITHUB\\WebCrawling-with-Python')
pdir = os.getcwd() ;print(pdir)

import pandas as pd
import requests # url 호출
from bs4 import BeautifulSoup as bs # html 태그 파싱
import random # 트래픽 조정 (기계가 아니라 사람이 읽는것처럼)
import time   # 트래픽 조정
from tqdm import tqdm, tqdm_notebook,tnrange # 진행상황 표현
import re # 정규표현식 regular expression 


#%% requests로 html 파일 불러오기
pnum = 1
year_month = 201906
base_url = f"https://www.innogov.go.kr/ucms/ogp/sug/list.do?pnum={pnum}&menuNo=300011&cateCd=&searchText=&status1Cd=&Status2Cd=&sugMonthTp={year_month}&orderKey=registDtDesc"
base_url

response = requests.get(base_url)
response # status code = 404 : 오류, 200 : 정상

if response.status_code == 200:
    html = bs(response.text, 'html.parser')
html # 페이지 소스코드 가져오기
    
#%% Beautifulsoup 을 통해 html 태그에서 href의 링크만 추출
# copy > copy selector
# content > div.suggestion_list > ul > li:nth-child(1) > dl > dt > p > a

if response.status_code == 200:
    html = bs(response.text, 'html.parser')
    tags = html.select('#content > div.suggestion_list > ul')[0].find_all('a')
tags # 이 중에 rink만 필요, list []
len(tags)

tags
print(isinstance(tags, (list)))
listdata = [1,2,3]
len(listdata)
type(listdata)

for tag in tags:
    print(tag['href'])

## 함수 : 연-월별 전체 제안 목록을 가져옵니다.
def get_suggestion_list(pnum) :
    base_url = f"https://www.innogov.go.kr/ucms/ogp/sug/list.do?pnum={pnum}&menuNo=300011&cateCd=&searchText=&status1Cd=&Status2Cd=&sugMonthTp={year_month}&orderKey=registDtDesc"
    response = requests.get(base_url)
    if response.status_code == 200:
        html = bs(response.text, 'html.parser')
        tags = html.select('#content > div.suggestion_list > ul')[0].find_all('a')
        if not tags :
            return(suggestion_list)
        else :
            for tag in tags:
                suggestion_list.append(tag['href']) # tag에 있는 href만 가져오기
        pnum += 1
        get_suggestion_list(pnum)
    else:
        return(suggestion_list)
        
suggestion_list = []
pnum = 1
get_suggestion_list(pnum)
print(len(suggestion_list))
suggestion_list[:3]
suggestion_list[25:30]

#%% BeautifulSoup 을 통해 html 태그를 파싱하기
url = suggestion_list[1]
base_url = f"https://www.innogov.go.kr{url}"
response = requests.get(base_url)
response # 200 : OK
html = bs(response.text, 'html.parser')
print(html)
# inspector(검사)를 이용하여 copy > copy selector # content > div.vveiw_box1 > dl > dt
html.select('#content > div.vveiw_box1 > dl > dt') # 리스트로 되어있다.
# title 가져오기        
title = html.select('#content > div.vveiw_box1 > dl > dt')[0].get_text(strip=True) # strip : 앞뒤 공백 제거
# 제안분야 가져오기                    
html.select('#content > div.vveiw_box1 > div.vveiw_name > ul > li:nth-child(1) > dl > dd')[0].get_text(strip=True)
                    
## id
u = 'view.do?menuNo=300011&sgId=216&pnum=1'
u.split('=')[2].split('&')[0] # id는 (0,1,2)번째에 있다. 게시글번호 '216'

## 함수 : 목록 리스트에 있는 url을 넘겨주면 내용을 크롤링 해옵니다.
def get_suggestion_content(url):
    article = []
    base_url = f"https://www.innogov.go.kr{url}"
    response = requests.get(base_url)
    if response.status_code == 200:
        html = bs(response.text, 'html.parser')
        title = html.select(
                '#content > div.vveiw_box1 > dl > dt')[0].get_text(strip=True)
        desc = html.select(
                '#content > div.vveiw_box1 > div.vveiw_name > ul > li > dl > dd')
        category = desc[0].get_text(strip=True)    
        start = desc[1].get_text(strip=True)
        end = desc[2].get_text(strip=True)
        author = desc[3].get_text(strip=True)
        content = html.select(
                 '#content > div.vveiw_box1 > div.vveiw_cont > div > pre ')[0].get_text(strip=True)          
        vote = html.select('#counter')[0].get_text(strip=True)
        sgId = url.split('=')[2].split('&')[0]
        
        article.append(sgId)
        article.append(title)
        article.append(category)
        article.append(content)
        article.append(start)
        article.append(end)
        article.append(vote)
        article.append(author)
        
        time.sleep(random.randint(1,2)) # 트래픽방지
        return article
    
## 각 게시물의 세부내용 가져오기
data = []
for i, suggestion in enumerate(tqdm(suggestion_list)):            # tqdm 이용 : 진행표시바 
    s = get_suggestion_content(suggestion)
    data.append(s)
## 데이터 프레임으로 만들기
column_names = ['sgId','title','category','content','start','end','vote','author']
data = pd.DataFrame(data,columns=column_names)
data.head()
data["category"].value_counts()
## csv 파일로 저장하기
data.to_csv("suggestion.csv",index=False)
data.shape
