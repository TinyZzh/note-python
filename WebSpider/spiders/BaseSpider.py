# -*- coding:UTF-8 -*-
import os

import requests
from bs4 import BeautifulSoup


class BaseSpider:
    def id(self):
        raise NotImplementedError("unimplemented method:id()")

    def run(self, _url_menu):
        menu = self.get_book_menu(_url_menu)
        for index, data in menu.items():
            _page_url = "{}/{}".format(_url_menu, data[0])
            _path = "{}_{}.txt".format(index, data[1])
            self.output(self.text(_page_url).encode("utf-8"), _path)

    def get_book_menu(self, url_menu):
        raise NotImplementedError("unimplemented method:get_book_menu()")

    def get_content(self, html):
        html_bf = BeautifulSoup(html)
        div_content = html_bf.find_all('div', id='content')
        return str(div_content[0].text)

    def replace_content(self, html):
        _content = html.replace('\xa0' * 4, '\n\n')
        return _content

    def text(self, _url):
        req = requests.get(url=_url)
        _html = req.content.decode(req.apparent_encoding)
        _result = self.get_content(_html)
        return self.replace_content(_result)

    def output(self, data, file_path):
        io_file = os.open(file_path, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
        try:
            os.write(io_file, data)
        finally:
            os.close(io_file)
        return
