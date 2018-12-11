# -*- coding:UTF-8 -*-
import logging
import sys
from multiprocessing.dummy import Pool as ThreadPool
from threading import Timer

from WebSpider.SpiderManager import SpiderManager

sm = SpiderManager()
pool = ThreadPool(5)


def _run(data):
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level='INFO', datefmt="[%Y-%m-%d %H:%M:%S]", format=log_format)
    try:
        spider = sm.get_spider_impl(data['id'])
        spider.run(**data['config'])
        pass
    except Exception as e:
        logging.error(e)
    pass


def _bootstrap():
    data = [
        {
            'id': 'www.biquge.info',
            'config': {'host': 'https://www.xbiquge6.com/', 'url_menu': '/77_77513/', 'output_path': '轮回乐园'}
        },
        {
            'id': 'www.biquge.info',
            'config': {'host': 'https://www.biquge.info/18_18728/', 'output_path': '重生完美时代'}
        },
        {
            'id': 'www.biqugexsw.com',
            'config': {'host': 'https://www.biqugexsw.com', 'url_menu': '/9_9107/', 'output_path': '余罪'}
        },
        {
            'id': 'www.xbiquge6.com',
            'config': {'host': 'https://www.xbiquge6.com', 'url_menu': '/79_79241/', 'output_path': '墨唐'}
        }
    ]
    try:
        pool.map(_run, data)
    finally:
        _submit_next_job()
    # _run()
    return 0


def _submit_next_job():
    t = Timer(300.0, _bootstrap)
    t.start()
    return


if __name__ == '__main__':
    sys.exit(_bootstrap())

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
