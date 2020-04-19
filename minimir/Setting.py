# -*- coding:UTF-8 -*-

import configparser
from datetime import datetime
#
# 挂机相关设置参数
#
from typing import List

from minimir.Struct import AccountConfig
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
    max_wk_time: int = 3600
    # 城池优先级
    city_type_weight_index: list = [2, 0, 1, 3, 4]
    # 自动整理背包出售的道具列表. 矿石
    bag_auto_sell_item_list: list = [219, 220, 221, 222]
    # 自动使用的道具列表. 1元宝
    bag_auto_use_item_list: list = [333, 234, 235, 236, 237, 238, 239, 407, 408]
    # 自动保存的仓库id
    auto_save_item_ku: int = 1

    def __init__(self) -> None:
        super().__init__()

    def load_setting(self) -> List[AccountConfig]:
        _file_path = 'conf/setting.ini'
        _config = configparser.ConfigParser()
        _config.read(_file_path, 'utf-8')
        _section = "default"
        if _config.has_section(_section):
            _annotations = self.__annotations__
            for r in _config.items(_section):
                field_name = r[0]
                field_val = r[1]
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
                    setattr(self, field_name, _val)
                pass
            pass
        accounts: List[AccountConfig] = []
        for account_section in _config.sections():
            if _section == account_section:
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
            _ac = AccountConfig(_user, _psw, _val, _md5, _ip)
            accounts.append(_ac)
            pass
        return accounts
