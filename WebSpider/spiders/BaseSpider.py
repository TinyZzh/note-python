# -*- coding:UTF-8 -*-
import os

import requests
from bs4 import BeautifulSoup


class BaseSpider:
    current_url = ''

    def id(self):
        raise NotImplementedError("unimplemented method:id()")

    # @param base_url 基础地址
    def run(self, base_url: str, url_menu='', base_path='./', offset=0, **kwargs):
        try:
            if not os.path.exists(base_path):
                os.makedirs(base_path)

            menu_list = self.get_book_menu("{}/{}".format(base_url, url_menu))
            for index in range(offset, len(menu_list)):
                _page_url = "{}/{}".format(base_url, menu_list[index][0])
                _path = "{}/{}_{}.txt".format(base_path, index, menu_list[index][1])
                try:
                    self.current_url = _page_url
                    self.output(self.text(_page_url).encode("utf-8"), _path)
                except Exception as e:
                    print(e)
                finally:
                    self.current_url = ''
                pass
        except Exception as e:
            print(e)

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
        req = requests.get(url=_url, headers=self.get_request_headers())
        _html = req.content.decode(req.apparent_encoding, 'ignore')
        _result = self.get_content(_html)
        return self.replace_content(_result)

    def output(self, data, file_path):
        io_file = os.open(file_path, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
        try:
            os.write(io_file, data)
        finally:
            os.close(io_file)
        return

    def get_request_headers(self):
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'zh-CN,zh;q=0.9',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/69.0.3497.81 Safari/537.36'}
        return headers

    def try_test(self):
        raise NotImplementedError("unimplemented method:try_test()")
