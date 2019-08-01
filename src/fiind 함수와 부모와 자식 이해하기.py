#!/usr/bin/env python
# coding: utf-8

# In[5]:


from urllib.request import urlopen
from bs4 import BeautifulSoup


# In[6]:


html = urlopen('https://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html, 'html.parser')


# In[7]:


nameList = bs.findAll('span', {'class': 'green'}) #bs.findALL(tagName, tagAttributes)
for name in nameList:
    print(name.get_text()) # tag를 제외하고 콘텐츠만 출력


# In[10]:


bs.findAll({'h1', 'h2', 'h3', 'h4'}) ### Or 연산으로 작동


# In[22]:


bs.findAll(id = 'title', class_='text') ### keyword 매개변수는 and 처럼 동작, class는 파이썬 예약어이므로 밑줄을 추가


# In[23]:


html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')


# In[31]:


for sibling in bs.find('table', {'id': 'giftList'}).tr: ### table에 가장 첫번째 tf tag를 가져옴. 근데 이게 테이블의 열 이름임. 사실상 필요없음
    print(sibling)


# In[30]:


for sibling in bs.find('table', {'id': 'giftList'}).tr.next_siblings: 
    print(sibling) 
    
### next_siblings를 통해 tr tag의 다음에 나오는 형제들만을 가져옴. 테이블의 1행을 버리고 2행부터 가져옴.
### next_sibling, previous_sibling, previous_siblings도 있다.


# In[28]:


for sibling in bs.find('table', {'id': 'giftList'}).findAll('tr', {'class':'gift'}):
    print(sibling)


# In[32]:


print(bs.find('img', {'src': '../img/gifts/img1.jpg'}).parent.previous_sibling.get_text()) 
### <img src = '../img/gifts/img1.jpg'를 찾고 그것의 부모인 태그인 td태그로 가서 바로 위의 형제인 가격이 적힌 td를 찾고 콘텐츠를 가져옴.

