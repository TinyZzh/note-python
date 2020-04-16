# -*- coding:UTF-8 -*-

import configparser
import ctypes
import random
import socket
import struct
from typing import Iterable


#
# 挂机相关设置参数
#
class Setting:
    # http伪造IP
    enable_random_client_ip: bool = False
    # 是否允许使用祭坛进度重置幻境. 缺省不启用
    enable_use_jt_exp: bool = False
    # 是否允许使用BOSS挑战券增加挑战boss的次数
    enable_use_boss_item: bool = False
    # 是否允许使用幻境重置券重置幻境
    enable_use_hj_item: bool = False
    # 推图BOSS连续失败阀值
    fight_fight_fail_threshold: int = 1000
    # 1秒对应的攻击回合数. 计算接口调用冷却时间
    each_second_delay_of_rounds: int = 7
    # 指定自动占领的城市类型. 默认无. 避免被攻占
    custom_city_type: int = -1
    # 城池优先级
    city_type_weight_index: list = [2, 0, 1, 3, 4]
    # 本次启动的临时客户端IP
    tmp_url_header_local_ip = None

    def __init__(self) -> None:
        super().__init__()

    def load_setting(self):
        _config = configparser.ConfigParser()
        _config.read('conf/setting.ini', 'utf-8')
        _section = "default"
        if _config.has_section(_section):
            # bool
            self.__reflection_set_property_value(_config, _section, [
                'enable_random_client_ip',
                'enable_use_jt_exp',
                'enable_use_boss_item',
                'enable_use_hj_item',
                'fight_fight_fail_threshold',
                'each_second_delay_of_rounds',
                'custom_city_type',
                'city_type_weight_index',
            ])
            pass
        if self.enable_random_client_ip:
            self.tmp_url_header_local_ip = Setting.get_random_ip()
        pass

    def __reflection_set_property_value(self, _config: configparser.ConfigParser, _section: str,
                                        properties: Iterable[str]):
        for prop_name in properties:
            if _config.has_option(_section, prop_name):
                _field_name = prop_name
                if hasattr(self, _field_name):
                    _val = None
                    if issubclass(type(getattr(self, _field_name)), bool):
                        _val = _config.getboolean(_section, prop_name)
                    elif issubclass(type(getattr(self, _field_name)), int):
                        _val = _config.getint(_section, prop_name)
                    elif issubclass(type(getattr(self, _field_name)), list):
                        _val = list(map(int, _config.get(_section, prop_name).split('|')))
                    else:
                        _val = _config.get(_section, prop_name)
                    setattr(self, _field_name, _val)
                    pass
                pass
            pass
        pass

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
        return Setting.long2ip(random.randint(_l, _r))

    @staticmethod
    def ip2long(ip_str: str):
        return struct.unpack("!I", socket.inet_aton(ip_str))[0]

    @staticmethod
    def long2ip(ip):
        return socket.inet_ntoa(struct.pack("!I", ip))
