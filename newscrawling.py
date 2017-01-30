from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import time
import requests
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
time.sleep(2)
url = 'http://news.naver.com/main/search/search.nhn?query=&ie=MS949'
driver.get(url)

def show_articles(keyword,date):
    #url = 'http://news.naver.com/main/search/search.nhn?query=&ie=MS949'
    driver.get(url)
    engine = driver.find_element_by_class_name('search_input')
    engine.clear()
    engine.send_keys(keyword)
    #time.sleep(2)
    datekey = driver.find_element_by_class_name('search_date_d')
    datekey.click()
    datekey.send_keys(date)
    input_date = driver.find_element_by_class_name('search_date')
    input_date.clear()
    input_date.send_keys(date,Keys.ENTER)
    return driver.current_url

neww=show_articles('도깨비', '2017-01-09')
driver.get(neww)

# article = driver.find_elements_by_class_name('tit')
# article_list = [x.text for x in article]
#
# link_list=[]
# for x in article:
#     link_list.append(x.get_attribute('href'))
# print(link_list)


# #총 페이지 계산하기
# article_listing =[]
# link_listing =[]
# paging=driver.find_elements_by_class_name('paging')
# pages = [x.text for x in paging]
# a=pages[-1].split(' ')
# a

URLS = []

last_page=driver.find_element_by_class_name('paging').find_elements_by_tag_name('a')
last = [x.text for x in last_page][-1].split('=')[-1]
#[x.text for x in last_page][-1].split('=')[-1]
while last == '다음' :
    last_page=driver.find_element_by_class_name('paging').find_elements_by_tag_name('a')
    last = [x.text for x in last_page][-1].split('=')[-1]
    #time.sleep(5)
    first_page=driver.current_url
    URLS.append(first_page)
    all_page =driver.find_element_by_class_name('paging').find_elements_by_tag_name('a')
    all_page1=[x.get_attribute('href') for x in all_page]
    URLS.extend(all_page1)
    last_page[-1].click()

while not last == '다음':
        first_page = driver.current_url
        URLS.append(first_page)
        all_page = driver.find_element_by_class_name('paging').find_elements_by_tag_name('a')
        all_page2 = [x.get_attribute('href') for x in all_page]
        URLS.extend(all_page2)
        print(last)
        break

len(all_page)
len(URLS)
#한 페이지 내용 긁어오기

aa = []
bb = []
cc = []
for a in URLS:
    response = requests.get(a)
    html = response.content
    soup = BeautifulSoup(html,'html.parser')
#what_i_found = soup.find_all('a')
    for a in soup.find_all('a',class_ = 'tit',href = True):
        print('Found the Title: ', a.text)
        print('Found the URL: ', a['href'])
        aa.append(a.text)
        bb.append(a['href'])
    for a in soup.find_all('div',class_='info'):
        print('Found the Press:', a.find(class_='press').text)
        cc.append(a.find(class_='press').text)

#csv 파일로 저장
df = pd.DataFrame({'기사명':aa,'링크': bb, '신문사':cc})
df
df.to_csv('news.csv',encoding='UTF-8')

