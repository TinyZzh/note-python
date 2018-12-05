# -*- coding:UTF-8 -*-
import logging
import sys
from multiprocessing.pool import Pool
from threading import Timer

from WebSpider.SpiderManager import SpiderManager


def _run(data):
    logging.basicConfig(level='INFO')
    try:
        sm = SpiderManager()
        spider = sm.get_spider_impl(data['id'])
        spider.run(**data['config'])
        pass
    except Exception as e:
        logging.error(e)
    finally:
        _submit_next_job(data)
    pass


def _submit_next_job(data):
    t = Timer(300.0, _run, [data])
    t.start()
    return


def bootstrap():
    # target = 'https://www.biquge.info/33_33149'
    # spider = WwwBiQuGeInfoSpider()
    # print(spider.run(target))

    data = [
        {
            'id': 'www.biquge.info',
            'config': {'host': 'https://www.xbiquge6.com/', 'url_menu': '/77_77513/', 'output_path': '轮回乐园'}
        },
        {
            'id': 'www.biquge.info',
            'config': {'host': 'https://www.biquge.info/18_18728/', 'output_path': '重生完美时代'}
        }
    ]
    pool = Pool(5)
    pool.map(_run, data)
    # _run()
    return 0


if __name__ == '__main__':
    sys.exit(bootstrap())

    # req = requests.get(url=target)

    # html = req.content.decode(req.apparent_encoding)

    # html_bf = BeautifulSoup(html)
    # # div_content = html_bf.find_all('div', id='content')
    # # txt = str(div_content[0].text).replace("笔～趣～阁ｗｗｗ.ｂiquge.ｉnfo", "")
    # # txt = txt.replace('\xa0' * 4, '\n\n')
    # menu_list = html_bf.select('div#list dl dd a')

    # for child in menu_list:
    #     print(child)

    # print(menu_list[0].text)
