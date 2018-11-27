# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup

from WebSpider.spiders.WwwBiQuGeInfoSpider import WwwBiQuGeInfoSpider

if __name__ == '__main__':
    target = 'https://www.biquge.info/33_33149'
    spider = WwwBiQuGeInfoSpider()
    print(spider.run(target))

    # req = requests.get(url=target)

    # html = req.content.decode(req.apparent_encoding)

    # html_bf = BeautifulSoup(html)
    # # div_content = html_bf.find_all('div', id='content')
    # # txt = str(div_content[0].text).replace("笔～趣～阁ｗｗｗ.ｂiquge.ｉnfo", "")
    # # txt = txt.replace('\xa0' * 4, '\n\n')
    # menu_list = html_bf.select('div#list dl dd a')

    # for child in menu_list:
    #     print(child)

    # print(menu_list[0].text)
