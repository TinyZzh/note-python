# -*- coding:UTF-8 -*-
import configparser
import copy
import ctypes
import datetime
import random
import socket
import struct
import typing

from minimir.Setting import Setting
from minimir.Struct import AccountConfig


class Utils:

    @staticmethod
    def reflect_set_field(objs: list, field_name: str, field_val: typing.Any):
        for obj in objs:
            _annotations = obj.__annotations__
            if field_name in _annotations:
                if _annotations[field_name] == bool:
                    _val = True if "1" == field_val or "true" == str(field_val).lower() else False
                elif _annotations[field_name] == int:
                    _val = int(field_val)
                elif _annotations[field_name] == float:
                    _val = float(field_val)
                elif _annotations[field_name] == datetime.datetime:
                    _val = datetime.datetime.strptime(field_val, "%Y-%m-%d %H:%M:%S")
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
    def to_datetime(str_datetime: str) -> datetime.datetime:
        return datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def to_datetime_str(dt: datetime.datetime) -> str:
        return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def load_account_setting() -> typing.List[AccountConfig]:
        _file_path = 'conf/setting.ini'
        _config = configparser.ConfigParser()
        _config.read(_file_path, 'utf-8')
        _section = "default"
        _base_setting = Setting()
        if _config.has_section(_section):
            _base_setting.resolve_init_options(_base_setting.__annotations__, _config.items(_section))
        accounts: typing.List[AccountConfig] = []
        for account_section in _config.sections():
            if _section == account_section:
                continue
            if _config.has_option(account_section, "enable") and not _config.getboolean(account_section, "enable"):
                continue
            _ip = _config.get(account_section, "client_ip")
            if _ip is not None and len(_ip) > 0:
                _ip = Utils.get_random_ip()
                _config.set(account_section, "client_ip", _ip)
                _config.write(open(_file_path, 'w'))
                pass
            _user = _config.get(account_section, "user")
            _psw = _config.get(account_section, "psw")
            _val = _config.get(account_section, "val")
            _md5 = _config.get(account_section, "md5")
            _pri_setting = copy.deepcopy(_base_setting)
            _pri_setting.resolve_init_options(_base_setting.__annotations__, _config.items(account_section))
            _ac = AccountConfig(_user, _psw, _val, _md5, _ip, _pri_setting)
            accounts.append(_ac)
            pass
        return accounts
