import logging
from datetime import datetime

from minimir import MiniMir, GamePlayer
from minimir.GameAction import GameAction
from minimir.Setting import Setting


class SignInAction(GameAction):
    #
    # 每日签到
    #
    __logger = logging.getLogger(__name__)
    # 当前签到的日期. 每日最多签到一次
    _cur_sign_date = None

    def __init__(self, client: MiniMir, p: GamePlayer, setting: Setting) -> None:
        super().__init__(client, p, setting)
        # 间隔3分钟(180s)检查一次
        self._run_delay = 180

    def evaluate(self) -> bool:
        _date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        if self._cur_sign_date == _date:
            return False
        p = self._player
        return not self.yield_wait_for() \
               and p.module_hj_completed and p.module_mj_completed \
               and p.module_yb_completed and p.module_fight_completed

    def execute(self) -> bool:
        # 签到
        if self.mir_req_once("user", "dayup"):
            p = self._player
            _date = datetime.strftime(datetime.now(), "%Y-%m-%d")
            self._cur_sign_date = _date
            # 重置各个模块的状态
            p.module_hj_completed = False
            p.module_yb_completed = False
            p.module_mj_completed = False
            p.module_fight_completed = False
            p.module_pk_completed = False
            self.__logger.info("==================={}:签到成功:{} ===================="
                               .format(self._cur_sign_date, self._player.name))
            pass
        else:
            self.__logger.info("=================== {}:今日已签到:{} ===================="
                               .format(self._cur_sign_date, self._player.name))
            pass
        #   膜拜沙城
        if self.mir_req_once("hh", "dayup"):
            self.__logger.info("=================== {}:行会签到成功:{} ===================="
                               .format(self._cur_sign_date, self._player.name))
            pass

        # 尝试完成成就
        prev_ts_ary = self.resp_struct_item_list(self.mir_req_once("item", "loaditem", type=5, ku=0))
        try:
            for attr_name in ["x1", "x2", "x3", "x4", "x5"]:
                self.try_attr_achievement(attr_name)
        except Exception as e:
            self.__logger.exception(e)
        finally:
            # rollback
            map(lambda bk: self.__logger.info(self.mir_req_once("item", "yong", id=bk.id, num=1, seat=0)), prev_ts_ary)
            pass

        self.auto_arrange_bag()
        return False

    def try_attr_achievement(self, attr_name: str) -> None:
        self.__logger.info("=================== {}:属性成就:{} ===================="
                           .format(self._player.name, attr_name))
        # 天书仓库
        ts_items = self.resp_struct_item_list(self.mir_req_once("item", "loaditem", type=5, ku=0))
        _total_attr = sum(map(lambda o: getattr(o, attr_name), ts_items))
        #
        bag_items = self.resp_struct_item_list(self.mir_req_once("item", "loaditem", type=1, ku=0))
        bag_items.extend(ts_items)
        _ts_ary = list(
            filter(lambda o: o.itemid == 698 and hasattr(o, attr_name) and getattr(o, attr_name) > 0, bag_items))
        _try_total_attr = sum(map(lambda o: getattr(o, attr_name), _ts_ary))
        # 当前属性不是最优. 需要换天书
        _ts_changed = False
        if _try_total_attr > _total_attr:
            # 先卸载全部天书
            for bk in ts_items:
                self.mir_req_once("item", "tsout", id=bk.id)
                pass
            for bk in _ts_ary:
                self.__logger.info(self.mir_req_once("item", "yong", id=bk.id, num=1, seat=0))
                pass
            _ts_changed = True
            pass
        # x1 => 5  x2 => 6
        _achieve_type = int(str(attr_name)[1]) + 4
        resp = self.mir_req_once("achieve", "load", type=_achieve_type)
        if resp:
            self.__logger.info(resp)
            pass
        if _ts_changed:
            for bk in ts_items:
                self.mir_req_once("item", "tsout", id=bk.id)
                pass
            pass
        self.__logger.info("attr:{} change completed. prev:{}, new:{}".format(attr_name, _total_attr, _try_total_attr))
        pass
