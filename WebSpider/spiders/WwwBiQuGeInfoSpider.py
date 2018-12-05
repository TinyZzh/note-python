# -*- coding:UTF-8 -*-
import re

import requests
from bs4 import BeautifulSoup

from WebSpider.spiders.BaseSpider import BaseSpider


#
# @version 2018.11.27
#
class WwwBiQuGeInfoSpider(BaseSpider):
    def id(self):
        return "www.biquge.info"

    def get_book_menu(self, url_menu):
        req = requests.get(url=url_menu, headers=self.get_request_headers())
        html = req.content.decode(req.apparent_encoding)
        html_bf = BeautifulSoup(html, self._bf4_parser())
        menu_list = html_bf.select('div#list dl dd a')

        _menu = []
        for data in menu_list:
            _menu.append((data['href'], data.text))
        return _menu

    def get_content(self, html):
        html_bf = BeautifulSoup(html, self._bf4_parser())
        div_content = html_bf.find_all('div', id='content')
        return str(div_content[0].text)

    def replace_content(self, html):
        _content = super(WwwBiQuGeInfoSpider, self).replace_content(html)
        _content = _content.replace('\xa0' * 4, '\n\n')
        #   示例:笔～趣～阁ｗｗｗ.ｂiquge.ｉnfo
        pattern = re.compile(r'笔[\S]趣[\S]阁[\S]{15}')
        _content = re.sub(pattern, '', _content)
        return _content

    def try_test(self):
        target = 'https://www.biquge.info/33_33149'
        spider = WwwBiQuGeInfoSpider()
        self._logger().info(spider.run(target, output_path="./x2/"))
        pass
