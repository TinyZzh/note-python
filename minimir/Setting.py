# -*- coding:UTF-8 -*-

import configparser
import ctypes
import random
import socket
import struct
from datetime import datetime
from typing import Iterable

#
# 挂机相关设置参数
#
from minimir.Utils import Utils


class Setting:
    # http伪造IP
    enable_random_client_ip: bool = False
    # 是否允许使用祭坛进度重置幻境. 缺省不启用
    enable_use_jt_exp: bool = False
    # 是否允许使用BOSS挑战券增加挑战boss的次数
    enable_use_boss_item: bool = False
    # 是否允许使用幻境重置券重置幻境
    enable_use_hj_item: bool = False
    # 启用自动整理背包.
    enable_auto_arrange_bag: bool = True
    # 自动出售矿石
    enable_auto_sell_ore: bool = True
    #
    threshold_smelting_equipment_lvl = 10
    # 推图BOSS连续失败阀值
    fight_fight_fail_threshold: int = 1000
    # 1秒对应的攻击回合数. 计算接口调用冷却时间
    each_second_delay_of_rounds: int = 7
    # 指定自动占领的城市类型. 默认无. 避免被攻占
    custom_city_type: int = -1
    # 最大行会挖矿时间. 自动结束挖矿并开启新挖矿. 单位：秒  86400 = 1d
    max_wk_time: int = 86400
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
            self.tmp_url_header_local_ip = Utils.get_random_ip()
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

