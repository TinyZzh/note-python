from dataclasses import dataclass
from datetime import datetime
from typing import List, Iterable

from minimir.Setting import Setting

equipment_attr = {
    # 攻击 - 魔法 - 道术 - 防御 - 魔防 - 幸运 - 速度 - 装备部位
    14: {'n': "布衣(男)", 'p': [4, 8, 0, 1, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0]},
    15: {'n': "布衣(女)", 'p': [4, 8, 0, 1, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0]},
    16: {'n': "木剑", 'p': [2, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    18: {'n': "青铜剑", 'p': [3, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    31: {'n': "匕首", 'p': [4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    17: {'n': "铁剑", 'p': [5, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    44: {'n': "乌木剑", 'p': [4, 8, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    40: {'n': "古铜戒指", 'p': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    43: {'n': "铁手镯", 'p': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]},
    70: {'n': "传统项链", 'p': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]},
    71: {'n': "小手镯", 'p': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]},
    72: {'n': "银手镯", 'p': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]},
    42: {'n': "金项链", 'p': [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]},
    700: {'n': "QQ群勋章", 'p': [5, 15, 5, 15, 5, 15, 0, 0, 0, 0, 0, 0, 0, 0]},
    47: {'n': "玻璃戒指", 'p': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]},

    1: {'n': "震天", 'p': [0, 0, 5, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    23: {'n': "短剑", 'p': [3, 11, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0]},
    1: {'n': "祈祷之刃", 'p': [8, 20, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0]},
    1: {'n': "井中月", 'p': [7, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "裁决之杖", 'p': [0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "命运之刃", 'p': [12, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "屠龙", 'p': [5, 35, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]},
    1: {'n': "黄金屠龙", 'p': [10, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},

    73: {'n': "大手镯", 'p': [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]},
    41: {'n': "青铜头盔", 'p': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]},
    56: {'n': "皮质手套", 'p': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]},
    65: {'n': "白金项链", 'p': [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    50: {'n': "六角戒指", 'p': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    58: {'n': "刚手镯", 'p': [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]},
    20: {'n': "轻型盔甲(女)", 'p': [0, 0, 0, 0, 0, 0, 3, 3, 1, 2, 0, 0, 0, 0]},
    19: {'n': "轻型盔甲(男)", 'p': [0, 0, 0, 0, 0, 0, 3, 3, 1, 2, 0, 0, 0, 0]},

    1: {'n': "生铁戒指", 'p': [0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]},
    1: {'n': "圣战头盔", 'p': [0, 2, 0, 0, 0, 0, 4, 5, 2, 5, 0, 0, 0, 0]},
    1: {'n': "圣战项链", 'p': [3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "圣战手镯", 'p': [2, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]},
    1: {'n': "圣战戒指", 'p': [0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]},

    1: {'n': "龙之戒指", 'p': [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "力量戒指", 'p': [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "泰坦戒指", 'p': [0, 0, 0, 0, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "龙之手镯", 'p': [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "心灵手镯", 'p': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "骑士手镯", 'p': [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "三眼手镯", 'p': [0, 0, 0, 0, 0, 1, 3, 1, 1, 0, 0, 0, 0, 0]},
    1: {'n': "绿色项链", 'p': [2, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "红宝石戒指", 'p': [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "铂金戒指", 'p': [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "思贝儿手镯", 'p': [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "紫碧螺", 'p': [0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "幽灵手套", 'p': [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0]},
    1: {'n': "恶魔铃铛", 'p': [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "幽灵项链", 'p': [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "生命项链", 'p': [0, 0, 1, 5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]},
    1: {'n': "天珠项链", 'p': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "灵魂项链", 'p': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    1: {'n': "default", 'p': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    2: [0, 0, 0, 0, 0, 0],
}


@dataclass()
class ItemProperties:
    pass


@dataclass
class AccountConfig(object):
    m_user: str
    m_psw: str
    m_val: str
    m_md5: str
    # 本次启动的临时客户端IP
    m_client_ip: str
    # 游戏设置
    m_setting: Setting


@dataclass()
class ItemInfo(object):
    # 物品唯一ID
    id: int
    area: int
    # 物品的模板表ID
    itemid: int
    # 装备穿戴的位置. 101：
    # 1: 武器  2：衣服  3：头盔  4：项链  5：勋章  6：左护腕  7：右护腕  8：左戒指  9：右戒指 10：莲花  11：腰带  12：鞋子  13：符文
    seat: int
    # 物品数量
    num: int
    time: int
    # 附加攻击属性
    x1: int
    # 魔法
    x2: int
    # 道术
    x3: int
    # 防御
    x4: int
    # 魔防
    x5: int
    # 幸运
    x6: int
    # 速度
    x7: int
    # 天赋类型  4:攻击  10：生命 13：速度
    g1: int
    # 天赋的数值
    g2: int
    # 符文
    slvl: int

    def __init__(self, args: Iterable = None) -> None:
        super().__init__()
        # 设置初始值
        for fn in self.__annotations__:
            setattr(self, fn, 0)

    #
    # def __gt__(self, other):
    #     if not isinstance(other, ItemInfo):
    #         raise TypeError('>运算对象是Card')
    #     if flowers.index(self.flower) > flowers.index(other.flower):
    #         return True
    #     elif flowers.index(self.flower) == flowers.index(other.flower) and \
    #             values.index(self.value) > values.index(other.value):
    #         return True
    #     else:
    #         return False
    #
    # def __eq__(self, other):
    #     if not isinstance(other, ItemInfo):
    #         raise TypeError('=运算要求目标是Card')
    #     if values.index(self.value) == values.index(other.value) and \
    #             flowers.index(self.flower) == flowers.index(other.flower):
    #         return True
    #     else:
    #         return False
    #
    # def __ge__(self, other):
    #     if not isinstance(other, ItemInfo):
    #         raise TypeError('>=运算要求目标是Card')
    #     return self > other or self == other

    @staticmethod
    def tpl_items() -> dict:
        return {
            217: "祝福油",
            223: "黑铁矿石",
            234: "强化攻击",
            235: "强化魔法",
            236: "强化道术",
            237: "强化生命",
            238: "强化防御",
            239: "强化魔防",
            319: "BOSS卷轴",
            333: "1元宝",
            339: "物资(千)",
            407: "防御心法",
            408: "魔防心法",
        }

    @staticmethod
    def tpl_item_attr(id: int):
        return None


@dataclass()
class CfgEquipmentInfo(object):
    id: int
    seat: int
    # 武器的性别. 0:通用 1:男 2:女
    sex: int
    name: str
    zhp: int
    zmp: int
    # 攻击
    za1: int
    za2: int
    # 魔法
    zb1: int
    zb2: int
    # 道术
    zc1: int
    zc2: int
    # 防御
    zd1: int
    zd2: int
    # 魔防
    ze1: int
    ze2: int
    # 幸运
    zf1: int
    # 速度
    speed: int
    # 天赋类型  4:攻击  10：生命 13：速度
    g1: int
    # 天赋的数值
    g2: int

    def __init__(self, args: List = None, info: ItemInfo = None) -> None:
        super().__init__()
        i = 0
        for fn in self.__annotations__:
            setattr(self, fn, args[i] if i in args else None)
            i += 1
            pass
        self.za2 += info.x1
        self.zb2 += info.x2
        self.zc2 += info.x3
        self.zd2 += info.x4
        self.ze2 += info.x5
        self.zf1 += info.x6
        self.speed += info.x7
        self.g1 += info.g1
        self.g2 += info.g2
        pass


#   行会信息
@dataclass
class HangHuiInfo:
    guaji: int
    guajitime: datetime
    # 最后一次同步行会信息的时间
    time_last_refresh: datetime
    # 是否有行会
    has_hh: bool

    def __init__(self) -> None:
        super().__init__()
        self.guaji = 0
        self.has_hh = False


@dataclass()
class BattleProperty:
    zhp: int = 0
    zmp: int = 0
    # 攻击
    za1: int = 0
    za2: int = 0
    # 魔法
    zb1: int = 0
    zb2: int = 0
    # 道术
    zc1: int = 0
    zc2: int = 0
    # 防御
    zd1: int = 0
    zd2: int = 0
    # 魔防
    ze1: int = 0
    ze2: int = 0
    # 幸运
    zf1: int = 0
    # 速度
    speed: int = 0

    # def __init__(self) -> None:
    #     super().__init__()


