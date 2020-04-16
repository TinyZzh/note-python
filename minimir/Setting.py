# -*- coding:UTF-8 -*-

import configparser
from typing import Iterable


#
# 挂机相关设置参数
#
class Setting:
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

    def __init__(self) -> None:
        super().__init__()

    def load_setting(self):
        _config = configparser.ConfigParser()
        _config.read('conf/setting.ini', 'utf-8')
        _section = "default"
        if _config.has_section(_section):
            # bool
            self.__reflection_set_property_value(_config, _section, [
                'enable_use_jt_exp',
                'enable_use_boss_item',
                'enable_use_hj_item',
                'fight_fight_fail_threshold',
                '1s_delay_of_rounds',
                'custom_city_type',
                'city_type_weight_index',
            ])
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
