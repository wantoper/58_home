import csv
import json
import os
import time

from lxml import etree
import requests
import re

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

def get_province():
    response = requests.get('https://www.58.com/changecity.html?catepath=house.shtml', headers=headers)
    html = response.text

    provinces = list()
    # 直辖市
    independentCityList = re.search("var independentCityList = {(.*?)}", html, re.I | re.S)
    independentCityListjson = json.loads(independentCityList.group().split("=")[1])
    for k, v in independentCityListjson.items():
        provinces.append((k, k, v.split("|")[0]))

    # 省份
    cityList = re.search("var cityList = {(.*?)</script>", html, re.I | re.S)
    citylistjson = json.loads(cityList.group().replace(" ", "").split("=")[1].replace("</script>", ""))
    del citylistjson["海外"]
    for province, citys in citylistjson.items():
        for city, acr in citys.items():
            provinces.append((province, city, acr.split("|")[0]))
    return provinces

def write_csv_home_info(headers:list,textlist:list):
    if not os.path.exists('58home_info.csv'):
        with open('58home_info.csv','a+',encoding='utf-8',newline='') as f:
             f_csv = csv.writer(f)
             f_csv.writerow(headers)

    with open('58home_info.csv', 'a+', encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(textlist)  # 逐行插入

def get_home(url,province,city,ifprint,outfile):
    print(province,city,url)
    response = requests.get(url,headers=headers)
    soup=etree.HTML(response.text)
    s1=soup.xpath('//div[@class="key-list imglazyload"]/div')
    for i in s1:
        try:
            home_name = i.xpath('.//span[@class="items-name"]/text()')[0]
            home_price_unit = i.xpath('.//p[@class="price"]/text()')
            home_price = i.xpath('.//p[@class="price"]/span/text()')
            if len(home_price) == 0:
                home_price = "暂无售价"
            else:
                home_price = home_price_unit[0] + home_price[0] + home_price_unit[1]

            categarys = i.xpath('.//a[@class="huxing"]/span')

            building_area="暂无内容"
            categary = "暂无内容"
            if len(categarys)>0:
                for s in categarys[:-1]:
                    categary=""
                    categary = categary + s.text + "/"
                categary = categary[:-1]
                building_area = categarys[-1].text


            statuss = i.xpath('.//a//div[@class="tag-panel"]/i')
            status = ""
            for s in statuss:
                status = status + s.text + "/"
            status = status[:-1]

            tags = i.xpath('.//div[@class="tag-panel"]/span')
            tag = ""
            for s in tags:
                tag = tag + s.text + "|"
            tag = tag[:-1]

            address = str(i.xpath('.//span[@class="list-map"]/text()')[0]).replace("[", "").replace("]","")\
                .strip().replace("\xa0", " ")
            address1 = address.split("  ")[0]
            addresss2 = address.split("  ")[1]

            home_info=dict(
                homename=home_name,
                homeproce=home_price,
                homecategory=categary,
                homebuilding_area=building_area,
                homestatus=status,
                hometag=tag,
                homeprovince=province,
                homecity=city,
                hometown=address1,
                homeaddress=addresss2
            )

            if ifprint:
                print(home_info)

            if outfile:
                write_csv_home_info(
                    headers=home_info.keys(),
                    textlist=home_info.values())


        except Exception as e:
            print(e.args)
            print("====出错问题页面:",province,city,url,home_name)
    s = soup.xpath('//a[@class="next-page next-link"]/@href')
    if (len(s) > 0):
        get_home(s[0], province, city, ifprint,outfile)
    else:
        print("爬取", province, city, "完毕!" + url)

if __name__ == "__main__":
    provinces = get_province()
    for province, city, arc in provinces[449:]:
        get_home("https://{}.58.com/xinfang/".format(arc), province, city,True,True)
    # get_home("https://sz.58.com/xinfang/","广东","深圳")
