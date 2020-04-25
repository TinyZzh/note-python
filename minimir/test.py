# -*- coding:UTF-8 -*-
import logging

from minimir.Struct import ItemInfo

if __name__ == "__main__":
    try:
        _info = ItemInfo(args=[1, 2, 3, 4])
    except Exception as e:
        logging.exception(e)
    pass
