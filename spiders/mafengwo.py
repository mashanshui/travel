import requests
from lxml import etree
import re


class MaFengWoSpiders(object):
    def __init__(self, city):
        self.city = city
        self.url_pattern = "http://www.mafengwo.cn/search/q.php?q=" + city + "&p={}&t=pois&kt=1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
        }
        pass

    def run(self):
        url_list = self.getUrlList()
        for url in url_list:
            page = self.getPageFromUrl(url)
            data = self.getDataFromPage(page)
        pass

    def getUrlList(self):
        url_list = []
        for i in range(1, 21):
            url = self.url_pattern.format(i)
            url_list.append(url)
        return url_list

    def getPageFromUrl(self, url):
        request = requests.get(url, headers=self.headers)
        return request.content.decode()

    def getDataFromPage(self, page):
        element = etree.HTML(page)
        lis = element.xpath('//*[@id="_j_search_result_left"]/div/div/ul/li')
        data_list = []
        for li in lis:
            item = {}
            # 景点名
            name = ''.join(li.xpath('./div/div[2]/h3/a/text()'))
            if len(name) == 0:
                continue
            item['name'] = name
            # 地址
            address = li.xpath('./div/div[2]/ul/li[1]/a/text()')[0]
            item['address'] = address
            # 点评数
            comments_num = li.xpath('./div/div[2]/ul/li[2]/a/text()')[0]
            item['comments_num'] = int(re.findall('蜂评\((\d+)\)', comments_num)[0])
            # 游记
            travel_num = li.xpath('./div/div[2]/ul/li[3]/a/text()')[0]
            item['travel_num'] = int(re.findall('游记\((\d+)\)', travel_num)[0])
            item['city'] = self.city
            data_list.append(item)
            print(item)
        return data_list


if __name__ == '__main__':
    ms = MaFengWoSpiders("安徽")
    ms.run()
