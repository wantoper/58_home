import json
from lxml import etree
import requests
import re

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}


def get(url):
    print(url)
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    s = html.xpath('//a[@class="next-page next-link"]/@href')
    if(len(s)>0):
        get(s[0])
    else:
        print("爬取结束最终页："+url)

if __name__ == "__main__":
    get("https://xiangxi.58.com/xinfang/")
