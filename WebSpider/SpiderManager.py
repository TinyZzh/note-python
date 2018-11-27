# -*- coding:UTF-8 -*-
from WebSpider.spiders import BaseSpider
from WebSpider.spiders.WwwBiQuGeInfoSpider import WwwBiQuGeInfoSpider


class SpiderManager():
    spiders = {}

    def __init__(self):
        lt = [WwwBiQuGeInfoSpider()]
        for spider in lt:
            self.register(spider)

    def register(self, spider):
        if spider is BaseSpider:
            self.spiders[spider.id()] = spider

    def getSpiderImpl(self, url):
        return self.spiders[url]
