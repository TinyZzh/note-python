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
import datetime


class GamePlayer:
    # 角色名
    name: str = ""
    # 用户唯一ID
    user_id: int
    level: int
    # 转生次数
    met: int
    # 存储的经验
    cbexp: int
    exp: int
    money: int
    # 元宝
    gold: int
    # 红包数量
    redbag: int
    # 战功
    war: int
    # 声望
    rep: int
    #
    # ========================== 挂机相关 ===================================
    is_guaji: bool
    guajimap: int
    guajitime: datetime
    # ========================== 幻境相关 ===================================
    # 幻境剩余挑战次数
    hj_num: int
    hj_lvl: int
    hj_top: int
    # ========================== 密境相关 ===================================
    mj_num: int
    mj_lvl: int
    mj_top: int
    # ========================== 押镖相关 ===================================
    yb_num: int
    yb_djnum: int
    # ========================== 推图相关 ===================================
    map: int
    # 挑战boss次数
    mapboss: int
    # ========================== PK相关 ===================================
    # PK剩余次数
    pknum: int

    # 称号等级
    title: int
    # 黄金宝箱打开次数
    bxnum: int

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
