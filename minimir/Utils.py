# -*- coding:UTF-8 -*-
import ctypes
import random
import socket
import struct
from datetime import datetime
from typing import Any


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
