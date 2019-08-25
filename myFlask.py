import json
from flask import Flask
from crawler.FscCrawler import FscCrawler

app = Flask(__name__)

# 取得網頁資料
@app.route('/website/fsc/content')
def getFscWebsiteContent():
    crawler = FscCrawler()
    urls = crawler.crawlUrls()
    datas = []
    for url in urls:
        c = crawler.crawlPageContent(url)
        datas.append(c)
    
    return json.dumps(datas, ensure_ascii=False)
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)
