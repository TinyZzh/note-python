# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup

from WebSpider.spiders.BaseSpider import BaseSpider


class WwwBiQuGeInfoSpider(BaseSpider):
    def id(self):
        return "www.biquge.info"

    def get_book_menu(self, url_menu):
        req = requests.get(url=url_menu)
        html = req.content.decode(req.apparent_encoding)
        html_bf = BeautifulSoup(html)
        menu_list = html_bf.select('div#list dl dd a')

        _menu = {}
        for i in range(len(menu_list)):
            _menu[i] = (menu_list[i]['href'], menu_list[i]['title'])
        return _menu

    def get_content(self, html):
        html_bf = BeautifulSoup(html)
        div_content = html_bf.find_all('div', id='content')
        return str(div_content[0].text)

    def replace_content(self, html):
        _content = super(WwwBiQuGeInfoSpider, self).replace_content(html)
        _content = _content.replace("笔～趣～阁ｗｗｗ.ｂiquge.ｉnfo", "")
        _content = _content.replace('\xa0' * 4, '\n\n')
        return _content
