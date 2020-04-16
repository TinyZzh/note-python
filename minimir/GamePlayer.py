# -*- coding:UTF-8 -*-


#
#   自动化脚本流程:
#
#   幻境          |   押镖  |   挖矿  |   推图挂机
#   推图BOSS      |
#   密境          |
#   Boss之家      |
#   世界Boss      |
#   劫镖          |
#
from datetime import datetime


# 战斗属性
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

    def __init__(self) -> None:
        super().__init__()


# 玩家数据
class GamePlayer:
    # 角色名
    name: str = ""
    # 用户唯一ID
    id: int = 0
    lvl: int = 0
    # 转生次数
    met: int = 0
    # 存储的经验
    cbexp: int = 0
    exp: int = 0
    money: int = 0
    # 元宝
    gold: int = 0
    # 红包数量
    redbag: int = 0
    # 战功
    war: int = 0
    # 声望
    rep: int = 0
    #
    # ========================== 挂机相关 ===================================
    guaji: bool = False
    guajimap: int = 0
    guajitime: datetime
    # ========================== 幻境相关 ===================================
    # 幻境剩余挑战次数
    hj_num: int = 0
    hj_lvl: int = 0
    hj_top: int = 0
    # ========================== 密境相关 ===================================
    mj_num: int = 0
    mj_lvl: int = 0
    mj_top: int = 0
    # ========================== 押镖相关 ===================================
    yb_num: int = 0
    yb_djnum: int = 0
    # ========================== 推图相关 ===================================
    map: int = 0
    # 挑战boss次数
    mapboss: int = 0
    # ========================== PK相关 ===================================
    # PK剩余次数
    pknum: int = 0

    # 称号等级
    title: int = 0
    # 黄金宝箱打开次数
    bxnum: int = 0
    # 挖矿等级
    wk_lvl: int = 0
    # 战斗属性
    unit: BattleProperty = BattleProperty()

    # ========================== 脚本 ===================================
    # 上次签到时间
    last_sign_in = None

    # 游戏模块
    # m - 幻境
    module_hj_completed: bool = False
    # m - 密境
    module_mj_completed: bool = False
    # m - 世界boss
    module_world_boss_completed: bool = False
    # m - 押镖
    module_yb_completed: bool = False
    # m - PK
    module_pk_completed: bool = False
    # m - 推图BOSS
    module_fight_completed: bool = False

    def __init__(self) -> None:
        super().__init__()
