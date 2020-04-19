# -*- coding:UTF-8 -*-
import ctypes
import random
import socket
import struct
from datetime import datetime
from functools import reduce
from typing import Any, Callable, List

from minimir.Struct import ItemInfo


class Utils:

    @staticmethod
    def reflect_set_field(objs: list, field_name: str, field_val: Any):
        for obj in objs:
            _annotations = obj.__annotations__
            if field_name in _annotations:
                if _annotations[field_name] == bool:
                    _val = True if "1" == field_val or "true" == str(field_val).lower() else False
                elif _annotations[field_name] == int:
                    _val = int(field_val)
                elif _annotations[field_name] == float:
                    _val = float(field_val)
                elif _annotations[field_name] == datetime:
                    _val = datetime.strptime(field_val, "%Y-%m-%d %H:%M:%S")
                else:
                    _val = field_val
                setattr(obj, field_name, _val)
                break
            pass
        return

    #
    # 随机生成一个国内的IP地址
    #
    @staticmethod
    def get_random_ip() -> str:
        pool = [
            [607649792, 608174079],  # /36.56.0.0-36.63.255.255
            [1038614528, 1039007743],  # /61.232.0.0-61.237.255.255
            [1783627776, 1784676351],  # /106.80.0.0-106.95.255.255
            [2035023872, 2035154943],  # /121.76.0.0-121.77.255.255
            [2078801920, 2079064063],  # /123.232.0.0-123.235.255.255
            [-1950089216, -1948778497],  # /139.196.0.0-139.215.255.255
            [-1425539072, -1425014785],  # /171.8.0.0-171.15.255.255
            [-1236271104, -1235419137],  # /182.80.0.0-182.92.255.255
            [-770113536, -768606209],  # /210.25.0.0-210.47.255.255
            [-569376768, -564133889],  # /222.16.0.0-222.95.255.255
        ]
        _pi = random.randint(0, len(pool) - 1)
        _l = ctypes.c_uint32(pool[_pi][0]).value
        _r = ctypes.c_uint32(pool[_pi][1]).value
        return Utils.long2ip(random.randint(_l, _r))

    @staticmethod
    def ip2long(ip_str: str):
        return struct.unpack("!I", socket.inet_aton(ip_str))[0]

    @staticmethod
    def long2ip(ip):
        return socket.inet_ntoa(struct.pack("!I", ip))

    @staticmethod
    def to_datetime(str_datetime: str) -> datetime:
        return datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def to_datetime_str(dt: datetime) -> str:
        return datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")

    #
    # item0是否比item1更好
    #
    @staticmethod
    def cmp_item(job: int, item0: ItemInfo, item1: ItemInfo) -> bool:
        _cfg0 = []
        _cfg1 = []
        # 装备0的总评分
        _i0_score = 0
        # 装备1的总评分
        _i1_score = 0
        _cmp_result = 0
        # 1. 幸运、速度
        if item0.x6 > item1.x6 or item0.x7 > item1.x7:
            return True

        # 2. 天赋优先.  天赋的占比增高
        # if item0.g1 == 2 and item1.g1 == 2:
        #     return item0.g2 > item1.g2
        # elif item0.g1 == 2:
        #     return True
        # elif item1.g1 == 2:
        #     return False
        _g_type = 4 if job == 1 else 2 if job == 2 else 3
        _offset = item0.g2 - item1.g2 if item0.g1 == _g_type and item1.g1 == _g_type else \
            item0.g1 if item0.g1 == _g_type else \
                -item1.g1 if item1.g1 == _g_type else 0
        if _offset != 0:
            return _offset > 0

        # 3. 检查装备的总属性收益 = 系数 + 基础属性
        _sum_xs_: Callable[[int, ItemInfo], List] = lambda j, i: (
            i.x1 if j == 1 else i.x2 if j == 2 else i.x3, i.x4, i.x5)
        _plus: Callable[[int, int], int] = lambda x, y: x + y
        # 根据职业的攻击属性
        _attr_list = [0, 1] if job == 1 else [2, 3] if job == 2 else [4, 5]
        # 防御、魔防
        _attr_list.extend([6, 7, 8, 9])
        _at0 = list(map(lambda i: _cfg0[i], _attr_list))
        _at0.extend(_sum_xs_(job, item0))
        _attr0 = reduce(_plus, _at0)
        _at1 = list(map(lambda i: _cfg1[i], _attr_list))
        _at1.extend(_sum_xs_(job, item1))
        _attr1 = reduce(_plus, _at1)
        if _attr0 == _attr1:
            # 4. 主属性收益 = 职业的攻击主属性

            _xs0_ = reduce(_plus, _sum_xs_(job, item0))
            _xs1_ = reduce(_plus, _sum_xs_(job, item1))
            # 5. 属性相同, 系数低的优先 - 成长空间大
            if _xs0_ < _xs1_:
                return True
        return _attr0 > _attr1
