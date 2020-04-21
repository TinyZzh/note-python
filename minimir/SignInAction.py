import logging
from datetime import datetime

from minimir import MiniMir, GamePlayer
from minimir.GameAction import GameAction


#
# 每日签到
#
class SignInAction(GameAction):
    __logger = logging.getLogger(__name__)
    # 当前签到的日期. 每日最多签到一次
    _cur_sign_date = None

    def __init__(self, client: MiniMir, p: GamePlayer) -> None:
        super().__init__(client, p)
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
            self.__logger.info("=================== 签到成功:{} ====================".format(self._cur_sign_date))
            pass
        else:
            self.__logger.info("=================== 今日已签到:{} ====================".format(self._cur_sign_date))
            pass
        #   膜拜沙城   TODO:
        if self.mir_req_once("user", "dayup"):
            self.__logger.info("=================== 膜拜成功:{} ====================".format(self._cur_sign_date))
            pass

        self.auto_arrange_bag()
        return False
