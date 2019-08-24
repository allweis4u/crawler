import os
import re
import time
import requests
from bs4 import BeautifulSoup

class CrawlerForFsc():
    
    def __init__(self):
        self.__mainLink = "https://www.fsc.gov.tw/ch/"
        self.__subLink = "home.jsp?id=131&parentpath=0,2"

    # 抓取網址列表
    def crawlUrls(self):
        page = 1 # 起始頁面
        tmpHtml = "" # 舊頁面

        url = self.__mainLink + self.__subLink
        newLinks = []
        while page < 2:
            time.sleep(1)

            # 爬取金管會裁罰案件
            payload = {
                "id": 131,
                "contentid": 131,
                "page": page,
                "parentpath": "0,2",
                "mcustomize": "multimessages_list.jsp"
            }
            r = requests.post(url, data=payload)
            soup = BeautifulSoup(r.text, features='lxml')
            content = soup.find_all("div", class_="page_content")[2]
            
            # page往後增加但是頁面不變時就跳出while迴圈
            if content == tmpHtml:
                break
            tmpHtml = content

            # 找出內容連結
            links = content.find_all('a')
            links = [l['href'] for l in links]

            # 串接網址
            tmpLinks = []
            for link in links:
                newLink = self.__mainLink + link
                tmpLinks.append(newLink)

            if len(tmpLinks) == 0:
                break

            newLinks += tmpLinks
            
            page += 1

        return newLinks

    # 抓取內頁
    def crawlPageContent(self, link):
        time.sleep(1)

        r = requests.post(link, data={})
        soup = BeautifulSoup(r.text, features='lxml')
        bsContent = soup.find("div", id="maincontent")

        if bsContent is None:
            errors = [
                "crawlPageContent", 
                "Not found maincontent where html = " + str(soup)
            ]
            raise Exception(",".join(errors))

        res = bsContent.find("div", class_="page_content").find_all("div")
        if len(res) < 2:
            errors = [
                "crawlWebsiteDoc",
                "Not found page_content where html = " + str(res)
            ]
            raise Exception(",".join(errors))

        return str(bsContent)



crawler = CrawlerForFsc()
urls = crawler.crawlUrls()
for url in urls:
    print(url)
    c = crawler.crawlPageContent(url)
    print(c)
    break
