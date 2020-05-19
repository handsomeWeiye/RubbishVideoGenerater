import newspaper
from  newspaper import Article
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time

# option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver =webdriver.Chrome(executable_path="chromedriver.exe",)


#爬取明星板块的热点 5188url
url = 'https://www.5ce.com/hot/5ce/2/7'

# 伪造请求头
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}

# requests请求网页
html = requests.get(url,headers=header)
# soup解析网页
soup = BeautifulSoup(html.text,'html.parser')



# 遍历解析构造json
def get_keywords (item):
    keywords = []
    vacabularys = item.find_all('a',attrs={"target":"_blank"})
    for vacabulary in vacabularys[0:5]:
        keywords.append(vacabulary.get_text())
    return keywords

def get_rel_url(url):
    res = requests.get(url,headers=header)
    soups = BeautifulSoup(res.text,'html.parser')
    # print(soups)
    rel_url = soups.find('span',class_="soucre").a.attrs['href']
    print(rel_url)
    return rel_url

def get_contents(item):
    contents = []
    content = {}
    items = item.find_all('li')
    for i in items:
        content['title'] = i.a.text
        content['url'] = 'https://www.5ce.com' + i.a['href']
        content['rel_url'] = get_rel_url(content['url'])
        contents.append(content)
    return contents

def get_topic(item):
    right =  item.find('div',class_="right")
    uls = right.find_all('p')
    topic = uls[1].text[5:]
    return topic


def get_result():
    res = []
    items = soup.findAll('dd',class_="read-item")
    for item in items:
        itemss = {}
        itemss['keywords'] = get_keywords(item)
        itemss['contents']  =  get_contents(item)
        itemss['topic'] = get_topic(item)
        res.append(itemss)
    return res

if __name__ == "__main__":

    # res =  get_result()



    url = r'https://www.5ce.com/view/5ce/1f93632a-8b95-ea11-8da3-20040ff9d71d/乔欣杨紫好朋友吗'
    res = driver.get(url)
    time.sleep(3)
    print(driver.find_element_by_class_name('content-detail').text)
    driver.close()

# print(news.url)
# #news.url为获取网址的url
    # print(news.text)
# # news.text为获取页面的所有text文字
# print(news.title)
# # news.title为获取页面的所有标题
# print(news.html)
# news.html为获取页面的所有源码
# print(news.authors)
# print(news.top_image)
# print(news.movies)
# print(news.keywords)
# print(news.summary)
# print(news.images)
# print(news.imgs)
