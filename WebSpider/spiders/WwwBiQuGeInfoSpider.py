# -*- coding:UTF-8 -*-
import re

from bs4 import BeautifulSoup

from WebSpider.spiders.BaseSpider import BaseSpider


#
# @version 2018.11.27
#
class WwwBiQuGeInfoSpider(BaseSpider):
    def id(self):
        return ["www.biquge.info", "www.xbiquge6.com", "www.biquyun.com", "www.kbiquge.com"]

    def _bf4_select_menu(self, bf: BeautifulSoup):
        return bf.select('div#list dl dd a')

    def get_content(self, html):
        html_bf = BeautifulSoup(html, self._bf4_parser())
        div_content = html_bf.find_all('div', id='content')
        if len(div_content) <= 0:
            self._logger().error("content is empty. id:{}, name:{}. html:{}".format(self.id(), self.name, html))
            return ""
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


#
# 第一个<dd>后面是最新章节.   第二个<dd>之后未实际章节内容
# https://www.biqugexsw.com/9_9107/
#
class WwwBiQuGeXswSpider(WwwBiQuGeInfoSpider):

    def id(self):
        return 'www.biqugexsw.com'

    def _bf4_select_menu(self, bf: BeautifulSoup):
        _list = []
        for dd in bf.find("div", 'listmain') \
                .select('dl > dt')[1] \
                .find_next_siblings('dd'):
            _list.append(dd.find('a'))
        return _list

    def try_test(self):
        target = 'https://www.biqugexsw.com/9_9107/'
        spider = WwwBiQuGeInfoSpider()
        print(spider.run(target, output_path="./x3/"))
        pass
