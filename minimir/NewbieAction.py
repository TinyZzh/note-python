# -*- coding:UTF-8 -*-
import logging
from datetime import datetime
from typing import List, Callable

from minimir import Struct
from minimir.BattleAction import BattleAction
from minimir.Utils import Utils


class NewbieAction(BattleAction):
    # 新账户引导
    # 1. 等级低于50级，转生等级0的新账户
    # 2. 优先挂机。 每间隔=((等级/10) + 1) * 10分钟. 自动换装，自动尝试过图
    __logger = logging.getLogger(__name__)

    def evaluate(self) -> bool:
        if self.yield_wait_for():
            return False
        # 转生低于1转、等级低于50级
        return self._player.met < 1 and self._player.lvl < 50

    def execute(self) -> bool:
        # 幻境 - 秘境 - 推图BOSS - PK -
        _battles: List[Callable] = [
            self.__newbie_upgrade__,
            self.__hj_fight,
            self.__mj_fight,
            self.__fight_fight,
        ]
        for func in _battles:
            if not func():
                break
        return True

    # 小号优先挂机为主. 每次半个小时
    # 装备提升之后尝试幻境战斗10次
    def __newbie_upgrade__(self) -> bool:
        if not self._player.guaji:
            self.mir_req("fight", "guaji", id=self._player.map)
            self._player.guajitime = datetime.now()
            pass
        _now_ = datetime.now()
        if (_now_ - self._player.guajitime).seconds > self._config.threshold_guaji_seconds:
            if self.mir_req_once("fight", "guajioff", id=self._player.map):
                self.auto_arrange_bag()
                pass
            if self.mir_req_once("fight", "guaji", id=self._player.map):
                self._player.guaji = True
                self._player.guajitime = _now_
                pass
            pass
        return False

    # 整理背包  -   有天赋和系数高的装备自动保存到仓库
    def auto_arrange_bag(self):
        self.__logger.info("=================== {}:新账户整理背包 =======================".format(self._player.name))
        # 玩家身上的装备
        self.refresh_body_item()
        # resp = self.mir_req("item", "loaditem", type=3, ku=0)
        # 仓库
        # resp = self.mir_req("item", "loaditem", type=2, ku=1)
        # 背包
        resp = self.mir_req_once("item", "loaditem", type=1, ku=0)
        if resp:
            _item_ary: List[Struct.ItemInfo] = []
            for _ri in resp['item']:
                _info = Struct.ItemInfo()
                for fn, fv in _ri.items():
                    Utils.reflect_set_field([_info], fn, fv)
                    pass
                _item_ary.append(_info)
                # 检查自动出售道具
                if _info.itemid in self._config.bag_auto_sell_item_list:
                    self.mir_req("item", "sell", id=_info.id, num=_info.num)
                    self.__logger.info("出售:{}, 数量:{}. info:{}".format(Struct.ItemInfo.tpl_items()[_info.itemid],
                                                                      _info.num, _info))
                # 检查自动使用的道具
                elif _info.itemid in self._config.bag_auto_use_item_list:
                    self.mir_req("item", "yong", id=_info.id, num=_info.num, seat=0)
                    self.__logger.info("使用:{}, 数量:{}. info:{}".format(Struct.ItemInfo.tpl_items()[_info.itemid],
                                                                      _info.num, _info))
                # 检查自动行会捐献 - 行会物资
                elif _info.itemid == 339:
                    if hasattr(self._player, 'hh') and self._player.hh is not None and self._player.hh.has_hh:
                        self.mir_req("hh", "gave", num=_info.num)
                        self.__logger.info("捐献:{}, 数量:{}. info:{}".format(Struct.ItemInfo.tpl_items()[_info.itemid],
                                                                          _info.num, _info))
                        pass
                    pass
                elif _info.itemid in Struct.equipment_attr and self._config.auto_use_better_equipment:
                    # 自动换装
                    if self._player.cmp_item(_info, ):
                        pass

                    pass
                # 检查自动保存. 幸运、天赋、总系数超过10
                elif _info.x6 > 0 or _info.g1 > 0 or (_info.x1 + _info.x2 + _info.x3 + _info.x4 + _info.x5) > 10:
                    # 从背包保存到仓库1
                    self.mir_req("item", "itemku", id=_info.id, type=1, ku=self._config.auto_save_item_ku)
                    _li = "保存:{}, 数量:{}. info:{}, 仓库:{}".format(Struct.ItemInfo.tpl_items()[_info.itemid],
                                                                _info.num,
                                                                _info, self._config.auto_save_item_ku)
                    self.__logger.info(_li)
                else:
                    pass
                pass

            # TODO: 将其余垃圾一键熔炼
            pass
        return
