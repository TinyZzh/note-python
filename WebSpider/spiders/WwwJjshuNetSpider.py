# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup

from WebSpider.spiders.BaseSpider import BaseSpider


#
# @version 2018.11.28
#
class WwwJjshuNetSpider(BaseSpider):
    def id(self):
        return "www.jjshu.net"

    def get_book_menu(self, url_menu):
        req = requests.get(url=url_menu, headers=self.get_request_headers())
        html = req.content.decode(req.apparent_encoding, 'ignore')
        html_bf = BeautifulSoup(html)
        menu_list = html_bf.select('div#readerlist ul li a')

        _menu = []
        for data in menu_list:
            _menu.append((data['href'], data.text))
        return _menu

    def get_content(self, html):
        html_bf = BeautifulSoup(html)
        div_content = html_bf.find_all('div', id='content')
        return str(div_content[0].text)

    def replace_content(self, html):
        _content = super(WwwJjshuNetSpider, self).replace_content(html)
        return _content

    def try_test(self):
        target = 'https://www.jjshu.net/'
        spider = WwwJjshuNetSpider()
        print(spider.run(target, url_menu='/2/2837/index.html', output_path="./xx/"))
        pass
