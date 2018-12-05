# -*- coding:UTF-8 -*-
import configparser
import logging
import os
import re

import requests
from bs4 import BeautifulSoup


class BaseSpider:
    # base info
    name = '',
    # config file *.ini
    config = [],
    config_file_path = '',

    # current calc
    current_url = '',
    # 是否正在运行
    is_running = False,

    logger = None

    def id(self):
        raise NotImplementedError("unimplemented method:id()")

    # @param host 基础地址
    def run(self, host: str, url_menu='', output_path='./', offset=0, node_name=None,
            config_file_path='./config/config.ini', **kwargs):
        # config
        self.name = output_path if node_name is None else node_name
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self.config.read(config_file_path, 'utf-8')

        if self.is_running is True:
            self._logger().info("spider is running. id:{}, name:{}".format(self.id(), self.name))
            return
        try:
            self.is_running = True
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            url = "{}/{}".format(host, url_menu)
            menu_list = self.get_book_menu(url)
            total_size = len(menu_list)
            if total_size <= 0:
                self._logger().info("unknown book menu. url:{}".format(url))
                return
            cur_index = self._get_cur_index()
            if cur_index >= total_size:
                self._logger().info("book:[{}] completed. cur_index:{} large than total:{}."
                                    .format(self.name, cur_index, total_size))
                return

            for index in range(offset, total_size):
                _page_url = "{}/{}".format(host, menu_list[index][0])
                _path = "{}/{}_{}.txt".format(output_path, index, self._cast_file_name(menu_list[index][1]))
                # if the output file is exist.
                if os.path.exists(_path) and os.path.getsize(_path) > 0:
                    continue
                try:
                    self.current_url = _page_url
                    self.output(self.text(_page_url).encode("utf-8"), _path)
                except Exception as e:
                    self._logger().error(e)
                finally:
                    self.current_url = ''
                pass
            # update config
            self._update_config(self.name, total_size)
        except Exception as e:
            self._logger().error(e)
        finally:
            self.is_running = False
        return

    # # #
    # 转换文件名称. 避免非法字符
    # # #
    def _cast_file_name(self, name):
        if name is None:
            return ""
        reg = re.compile(r'[\\/:*?"<>|\r\n]+')
        ary = reg.findall(name)
        if ary:
            for nv in ary:
                name = name.replace(nv, "_")
        return name

    def _get_cur_index(self):
        return self.config.getint(self.name, 'index') if self.config.has_option(self.name, 'index') else 0

    def _update_config(self, source, index):
        if not self.config.has_section(self.name):
            self.config.add_section(self.name)
        self.config.set(self.name, "source", str(source))
        self.config.set(self.name, "index", str(index))
        with open(self.config_file_path, 'w', encoding='utf-8') as file:
            self.config.write(file)
        pass

    def get_book_menu(self, url_menu):
        req = requests.get(url=url_menu, headers=self.get_request_headers())
        html = req.content.decode(req.apparent_encoding, 'ignore')
        html_bf = BeautifulSoup(html, self._bf4_parser())
        menu_list = self._bf4_select_menu(html_bf)

        _menu = []
        for data in menu_list:
            _menu.append((data['href'], data.text))
        return _menu

    def _bf4_select_menu(self, bf: BeautifulSoup):
        raise NotImplementedError("unimplemented method:_bf_select_menu()")

    def get_content(self, html):
        html_bf = BeautifulSoup(html, self._bf4_parser())
        div_content = html_bf.find_all('div', id='content')
        if len(div_content) <= 0:
            self._logger().error("unknown content. {}".format(html))
        return str(div_content[0].text)

    def _bf4_parser(self):
        return 'lxml'

    def replace_content(self, html):
        _content = html.replace('\xa0' * 4, '\n')
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

    def _logger(self):
        if self.logger is None:
            self.logger = logging.getLogger(self.id())
        return self.logger

    def try_test(self):
        raise NotImplementedError("unimplemented method:try_test()")
