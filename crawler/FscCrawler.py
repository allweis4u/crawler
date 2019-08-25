import os
import re
import time
import requests
from bs4 import BeautifulSoup

class FscCrawler():
    
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
    def crawlPageContent(self, url):
        results = {}
        results["url"] = url

        r = requests.post(url, data={})
        soup = BeautifulSoup(r.text, features='lxml')
        mainSoup = soup.find("div", id="maincontent")

        # 取出標題
        titleObj = mainSoup.find("h3")
        if titleObj:
            results["title"] = titleObj.get_text().strip()
        
        # 取出內文
        contentObj = mainSoup.find(class_="page_content")
        contentObj.find(class_="contentdate").extract() # 把日期抽掉
        #results["content"] = contentObj.get_text().strip()
        results["content"] = self.trimHtmlTags( str(contentObj) ).strip()
        
        return results

    # 去除Html tag
    def trimHtmlTags(self, text):
        text = re.sub(r"</?(div|p)[^<]*>|<br/>", "\n", text) # 取代成換行
        text = re.sub(r"</?[^<]*>", "", text)
        return text

