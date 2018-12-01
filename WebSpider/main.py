# -*- coding:UTF-8 -*-

import sys
from threading import Timer

from WebSpider.SpiderManager import SpiderManager


def _run():
    try:
        sm = SpiderManager()
        spider = sm.get_spider_impl("www.jjshu.net")
        spider.run(base_url='https://www.jjshu.net', url_menu='/2/2837/index.html', base_path='轮回乐园')
        pass
    except Exception as e:
        print(e)
    finally:
        _submit_next_job()
    pass


def _submit_next_job():
    t = Timer(60.0, _run)
    t.start()
    return


def bootstrap():
    # target = 'https://www.biquge.info/33_33149'
    # spider = WwwBiQuGeInfoSpider()
    # print(spider.run(target))

    _run()
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
