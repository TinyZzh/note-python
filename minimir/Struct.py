from dataclasses import dataclass


@dataclass()
class ItemInfo:
    # 物品唯一ID
    id: int
    area: int
    # 物品的模板表ID
    itemid: int
    # 装备穿戴的位置.
    #
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
    # 天赋类型
    g1: int
    # 天赋的数值
    g2: int

    def __init__(self) -> None:
        super().__init__()
        # 设置初始值
        for f in ["id", "area", "itemid", "seat", "num", "time", "x1", "x2", "x3", "x4", "x5", "x6", "g1", "g2"]:
            setattr(self, f, 0)

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
