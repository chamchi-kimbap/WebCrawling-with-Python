#!/usr/bin/env python
# coding: utf-8

# In[1]:


from urllib.request import urlopen
from bs4 import BeautifulSoup


# In[21]:


html = urlopen("http://www.pythonscraping.com/pages/page1.html")


# In[20]:


bs = BeautifulSoup(html.read(), 'html.parser')


# In[18]:


print(bs.h1)


# In[ ]:


html = urlopen("http://www.pythonscraping.com/pages/page1.html") ### html 매번 다시해줘야 제대로 작동?


# In[22]:


bs = BeautifulSoup(html, 'html.parser') ### html.parser : 구문분석기


# In[24]:


print(bs.html.h1) ###


# In[26]:


from urllib.request import HTTPError ### 페이지를 찾을 수 없어가, URL 해석에서 에러가 생기는 경우 발생하는 에러


# In[28]:


try:
    html = urlopen('http://www.pythonscraping.com/pages/error.html')
except HTTPError as e:
    print(e)


# In[29]:


from urllib.error import URLError ### 웹페이지가 다운됐거나 URL에 오타가 있을 때, URLError 발생


# In[30]:


try:
    html = urlopen('https://pythonscrapingthisurldoesnotexist.com')
except HTTPError as e:
    print(e)
except URLError as e:
    print('The server could not be found!')
else:
    print('It Worked!')


# In[37]:


print(bs.nonExistentTag)


# In[31]:


# print(bs.nonExistentTag.someTag) ### 존재하지 않는 태그를 불러서 함수를 호출하면 발생하는 에러 AttributeError


# In[32]:


try:
    badContent = bs.nonExistingTag.anotherTag
except AttributeError as e:
    print("Tag was not found")
else:
    if badContent == None:
        print("Tag was not found")
    else:
        print(badContent)


# In[34]:


from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
        title = bs.body.h1
    except AttributeError as e:
        return None
    return title

title = getTitle('http://www.pythonscraping.com/pages/page1.html')
if title == None:
    print('Title could not be found')
else:
    print(title)

