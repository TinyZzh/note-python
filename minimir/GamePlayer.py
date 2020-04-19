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
import logging
from dataclasses import dataclass
from datetime import datetime
# 战斗属性
from typing import Dict

import requests

from minimir import MiniMir
from minimir.Struct import ItemInfo, AccountConfig


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
