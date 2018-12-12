# -*- coding:UTF-8 -*-

from bs4 import BeautifulSoup

from WebSpider.spiders.BaseSpider import BaseSpider


#
# @version 2018.11.28
#
class WwwJjshuNetSpider(BaseSpider):
    def id(self):
        return "www.jjshu.net"

    def _bf4_select_menu(self, bf: BeautifulSoup):
        return bf.select('div#readerlist ul li a')

    def get_content(self, html):
        html_bf = BeautifulSoup(html, self._bf4_parser())
        div_content = html_bf.find_all('div', id='content')
        if len(div_content) <= 0:
            self._logger().error("content is empty. id:{}, name:{}. html:{}".format(self.id(), self.name, html))
            return ""
        return str(div_content[0].text)

    def replace_content(self, html):
        _content = super(WwwJjshuNetSpider, self).replace_content(html)
        return _content

    def try_test(self):
        target = 'https://www.jjshu.net/'
        spider = WwwJjshuNetSpider()
        self._logger().info(spider.run(target, url_menu='/2/2837/index.html', output_path="./xx/"))
        pass
