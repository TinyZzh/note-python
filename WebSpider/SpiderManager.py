# -*- coding:UTF-8 -*-
from WebSpider.spiders import BaseSpider
from WebSpider.spiders.WwwBiQuGeInfoSpider import WwwBiQuGeInfoSpider, WwwBiQuGeXswSpider
from WebSpider.spiders.WwwJjshuNetSpider import WwwJjshuNetSpider


class SpiderManager():
    spiders = {}

    def __init__(self):
        lt = [WwwBiQuGeInfoSpider(), WwwJjshuNetSpider(), WwwBiQuGeXswSpider()]
        for spider in lt:
            self.register(spider)

    def register(self, spider):
        if isinstance(spider, BaseSpider.BaseSpider):
            _id = spider.id()
            if type(_id) is list:
                for key in _id:
                    self.spiders[key] = type(spider)
            else:
                self.spiders[_id] = type(spider)

    def get_spider_impl(self, url):
        return self.spiders[url]()
