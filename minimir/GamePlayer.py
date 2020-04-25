# -*- coding:UTF-8 -*-


# 战斗属性
import functools
import logging
import typing
from datetime import datetime
from typing import Dict

import requests

from minimir import MiniMir, Struct
from minimir.Struct import BattleProperty, ItemInfo, AccountConfig, HangHuiInfo, CfgEquipmentInfo


# 玩家数据
class GamePlayer:
    __logger = logging.getLogger(__name__)
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

    job: int = 0
    # 性别. 1:男性
    sex: int = 1
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
    # 身上穿戴的装备
    #
    body_item: Dict[int, ItemInfo]

    # ========================== 脚本 ===================================
    # 客户端
    client: MiniMir
    # 账号相关配置
    acc_config: AccountConfig
    # 行会信息
    hh: HangHuiInfo
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

    def __init__(self, client: MiniMir, ac: AccountConfig) -> None:
        super().__init__()
        self.client = client
        self.acc_config = ac
        pass

    # 调用接口
    # md5(1079296108 + BFEBFBFF + 000306C3)  => d43228ea4953279321578cc6a4dc18f8
    # _base_secret = 'd43228ea4953279321578cc6a4dc18f8'
    def mir_request(self, module, action, **kargs):
        _params = {}
        _params = kargs if kargs is not None else {}
        _params["m"] = module
        _params["a"] = action
        if "without_md5" in kargs:
            del _params["without_md5"]
        else:
            _params["md5"] = self.acc_config.m_md5
            pass

        _url_extra = []
        for k, v in kargs.items():
            _url_extra.append("{}={}".format(k, v))
            pass

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
            "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, "
                      "application/vnd."
                      "ms-excel, application/vnd.ms-powerpoint, application/msword, */*"
        }
        # 简单的伪造IP   - hping3伪造源IP   - REMOTE_ADDR
        if self.client.setting.enable_random_client_ip:
            headers["CLIENT-IP"] = self.acc_config.m_client_ip
            headers["X-FORWARDED-FOR"] = self.acc_config.m_client_ip
            headers["X-REAL-IP"] = self.acc_config.m_client_ip
            pass
        self.__logger.debug("[request] module:{}, action:{}, kargs:{}".format(module, action, kargs))
        r = requests.post("{}?{}".format(self.client.host, "&".join(_url_extra)), data=_params, headers=headers)
        if r.status_code == requests.codes.ok:
            resp = r.json()
            # if resp['b'] != 1:
            #     self.__logger.debug(resp)
            return resp
        else:
            r.raise_for_status()
        return

    #
    # item0是否比item1更好
    #
    def cmp_item(self, item0: ItemInfo, item1: ItemInfo) -> bool:
        _cfg0 = CfgEquipmentInfo(Struct.equipment_attr[item0.itemid])
        if _cfg0.sex != 0 and _cfg0.sex != self.sex:
            return False
        _cfg1 = CfgEquipmentInfo(Struct.equipment_attr[item1.itemid])

        job = self.job

        # 装备0的总评分
        _i0_score = 0
        # 装备1的总评分
        _i1_score = 0
        _cmp_result = 0
        # 1. 幸运、速度
        if item0.x6 > item1.x6 or item0.x7 > item1.x7:
            return True

        # 2. 天赋优先.  天赋的占比增高
        # if item0.g1 == 2 and item1.g1 == 2:
        #     return item0.g2 > item1.g2
        # elif item0.g1 == 2:
        #     return True
        # elif item1.g1 == 2:
        #     return False
        _g_type = 4 if job == 1 else 2 if job == 2 else 3
        _offset = item0.g2 - item1.g2 if item0.g1 == _g_type and item1.g1 == _g_type else \
            item0.g1 if item0.g1 == _g_type else \
                -item1.g1 if item1.g1 == _g_type else 0
        if _offset != 0:
            return _offset > 0

        # 3. 检查装备的总属性收益 = 系数 + 基础属性
        _sum_xs_: typing.Callable[[int, ItemInfo], typing.List] = lambda j, i: (
            i.x1 if j == 1 else i.x2 if j == 2 else i.x3, i.x4, i.x5)
        _plus: typing.Callable[[int, int], int] = lambda x, y: x + y
        # 根据职业的攻击属性
        _attr_list = [0, 1] if job == 1 else [2, 3] if job == 2 else [4, 5]
        # 防御、魔防
        _attr_list.extend([6, 7, 8, 9])
        _at0 = list(map(lambda i: _cfg0[i], _attr_list))
        _at0.extend(_sum_xs_(job, item0))
        _attr0 = functools.reduce(_plus, _at0)
        _at1 = list(map(lambda i: _cfg1[i], _attr_list))
        _at1.extend(_sum_xs_(job, item1))
        _attr1 = functools.reduce(_plus, _at1)
        if _attr0 == _attr1:
            # 4. 主属性收益 = 职业的攻击主属性

            _xs0_ = functools.reduce(_plus, _sum_xs_(job, item0))
            _xs1_ = functools.reduce(_plus, _sum_xs_(job, item1))
            # 5. 属性相同, 系数低的优先 - 成长空间大
            if _xs0_ < _xs1_:
                return True
        return _attr0 > _attr1
