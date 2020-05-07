# -*- coding:UTF-8 -*-

#
# 挂机相关设置参数
#
import datetime
import typing


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
    # 城池被攻击. 自动占领新城池. 从最弱的开始. 恶心对手
    enable_city_fuck_off_protect: bool = True
    # 自动找空余的城池. False时自动攻击比玩家实力低的城池
    only_lookup_empty_city: bool = True
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
    # 挂机时间的阀值
    threshold_guaji_seconds: int = 1800
    # 自动使用更好的装备
    auto_use_better_equipment: bool = False

    def __init__(self) -> None:
        super().__init__()
        pass

    def resolve_init_options(self, anns_dict: typing.Dict[str, any], items: typing.List[any]) -> None:
        for r in items:
            _field_name = r[0]
            _field_val = r[1]
            if _field_name in anns_dict:
                if anns_dict[_field_name] == bool:
                    _val = True if "1" == _field_val or "true" == str(_field_val).lower() else False
                elif anns_dict[_field_name] == int:
                    _val = int(_field_val)
                elif anns_dict[_field_name] == float:
                    _val = float(_field_val)
                elif anns_dict[_field_name] == datetime.datetime:
                    _val = datetime.datetime.strptime(_field_val, "%Y-%m-%d %H:%M:%S")
                elif anns_dict[_field_name] == list:
                    _val = list(map(int, str.split(_field_val, "|")))
                else:
                    _val = _field_val
                setattr(self, _field_name, _val)
            pass
        return
