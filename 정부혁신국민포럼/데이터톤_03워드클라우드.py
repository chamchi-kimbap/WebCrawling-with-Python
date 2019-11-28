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


#%% WordCloud 함수 생성
from wordcloud import WordCloud , STOPWORDS
import matplotlib.pyplot as plt

def displayWordCloud(data=None, backgroundcolor = 'white', width=1600, height=800):
    wordcloud = WordCloud( font_path = '/Library/Fonts/NanumBarunGothic.ttf',
                           stopwords = STOPWORDS,
                           background_color = backgroundcolor,
                           width = width, height=height ).generate(data)
    plt.figure(figsize = (15,10))
    plt.imshow(wordcloud)
    plt.aixs("off")
    plt.show()

#%% 명사 추출
    
from konlpy.tag import Twitter  # 한글 형태소 분석기 
twit = Twitter()    
print(twit.pos("히라마블로그에온걸환영해!"))
 
#df['content'].fillna('')  # 비어있는 content를 ''로 대체
#str(df['content'].fillna('')) # 읽기 편하게 변환?
#''.join(str(df['content'].fillna('')))
#twit.nouns(''.join(str(df['content'].fillna(''))))
 
%time twit_content_pos = twit.nouns(''.join(str(df['content'].fillna('')))) # 명사(nouns)추출 
twit_content_pos[-10:] 


#%% twit 으로 워드클라우드 그리는 함수
def twit_nouns_wordcloud(content) :
    twit_content_nouns = twt.nouns(''.join(str(df['content'].fillna(''))))
    displayWordCloud(' '.join(twit_content_nouns))
    
twit_nouns_wordcloud(df['content'])
