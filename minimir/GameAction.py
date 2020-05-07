# -*- coding:UTF-8 -*-
import logging
import time
from collections import Iterable
from typing import List, Dict, Callable

from minimir import MiniMir, Setting, Struct
from minimir.GamePlayer import GamePlayer
from minimir.Struct import ItemInfo
from minimir.Utils import Utils


class GameAction:
    __logger = logging.getLogger(__name__)
    # 客户端
    _m_client: MiniMir
    # 用户信息
    _player: GamePlayer
    # 挂机设置
    _config: Setting

    # 间隔执行. 避免太频繁的调用接口
    _last_run_timestamp = -1
    _run_delay = -1

    def __init__(self, client: MiniMir, p: GamePlayer, setting: Setting) -> None:
        super().__init__()
        self._m_client = client
        self._player = p
        self._config = setting

    def evaluate(self) -> bool:
        raise NotImplementedError("unimplemented method:evaluate()")

    def execute(self) -> bool:
        raise NotImplementedError("unimplemented method:execute()")

    def client(self) -> MiniMir:
        return self._m_client

    def mir_req(self, module, action, **kargs):
        return self._player.mir_request(module, action, **kargs)

    def mir_req_once(self, module, action, feedback: [Iterable, Callable[[object], None]] = None, **kargs) -> [(
            bool, object), None]:
        _resp = self._player.mir_request(module, action, **kargs)
        _suc = _resp is not None and 'b' in _resp and _resp['b'] == 1
        if _suc:
            if feedback is not None:
                if isinstance(feedback, Iterable):
                    map(lambda f: f(_resp), feedback)
                elif callable(feedback):
                    feedback(_resp)
                    pass
                else:
                    raise Exception("unknown feedback type:{}".format(type(feedback)))
        else:
            logging.debug("action:{}, response:{}".format(action, str(_resp)))
            pass
        return _resp if _suc else None

    def use_item(self, tid: int, amount: 1):
        return

    # 初始化玩家身上的装备
    def refresh_body_item(self):
        seats: Dict[int, ItemInfo] = {}
        self.__logger.info("=================== {}:同步玩家身上的装备 =======================".format(self._player.name))
        resp = self.mir_req("item", "loaditem", type=3, ku=0)
        if resp is not None and "b" in resp and resp['b'] == 1:
            for _ri in resp['item']:
                _info = Struct.ItemInfo()
                for fn, fv in _ri.items():
                    Utils.reflect_set_field([_info], fn, fv)
                    pass
                seats[_info.seat] = _info
                pass
            self._player.body_item = seats
            pass
        return

    # 整理背包  -   有天赋和系数高的装备自动保存到仓库
    def auto_arrange_bag(self):
        self.__logger.info("=================== {}:自动整理背包 =======================".format(self._player.name))
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
                    self.__logger.info("{}:出售:{}, 数量:{}. info:{}"
                                       .format(self._player.name, Struct.ItemInfo.tpl_items()[_info.itemid],
                                               _info.num, _info))
                # 检查自动使用的道具
                elif _info.itemid in self._config.bag_auto_use_item_list:
                    self.mir_req("item", "yong", id=_info.id, num=_info.num, seat=0)
                    self.__logger.info("{}:使用:{}, 数量:{}. info:{}"
                                       .format(self._player.name, Struct.ItemInfo.tpl_items()[_info.itemid], _info.num,
                                               _info))
                # 检查自动行会捐献 - 行会物资
                elif _info.itemid == 339:
                    if hasattr(self._player, 'hh') and self._player.hh is not None and self._player.hh.has_hh:
                        self.mir_req("hh", "gave", num=_info.num)
                        self.__logger.info("():捐献:{}, 数量:{}. info:{}".format(self._player.name,
                                                                             Struct.ItemInfo.tpl_items()[_info.itemid],
                                                                             _info.num, _info))
                        pass
                    pass
                elif self._config.auto_use_better_equipment:
                    # 自动换装
                    # if Utils.cmp_item(self._player.job, _info, ):

                    pass
                # 检查自动保存. 幸运、天赋、总系数超过10
                elif _info.x6 > 0 or _info.g1 > 0 or (_info.x1 + _info.x2 + _info.x3 + _info.x4 + _info.x5) > 10:
                    # 从背包保存到仓库1
                    self.mir_req("item", "itemku", id=_info.id, type=1, ku=self._config.auto_save_item_ku)
                    _li = "{}:保存:{}, 数量:{}. info:{}, 仓库:{}".format(self._player.name,
                                                                   Struct.ItemInfo.tpl_items()[_info.itemid], _info.num,
                                                                   _info, self._config.auto_save_item_ku)
                    self.__logger.info(_li)
                else:
                    pass
                pass

            # TODO: 将其余垃圾一键熔炼
            pass
        return

    #
    #   是否需要等待一段时间?
    #
    def yield_wait_for(self) -> bool:
        if self._run_delay <= 0:
            return False
        _timestamp = time.time()
        _offset = _timestamp - self._last_run_timestamp
        if _offset >= self._run_delay:
            self.__logger.debug("--------------------- {}:{}, {} ------------------------"
                                .format(self._player.name, type(self), _offset))
            self._last_run_timestamp = _timestamp
            return False
        else:
            return True

    # 使用道具
    def __try_use_hj_item(self) -> bool:
        # 4. 使用幻境重置券
        if self._config.enable_use_hj_item:
            #  TODO: 未实现
            pass
        return
