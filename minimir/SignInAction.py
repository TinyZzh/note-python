import logging
from datetime import datetime

from minimir import MiniMir
from minimir.GameAction import GameAction


#
# 每日签到
#
class SignInAction(GameAction):
    __logger = logging.getLogger(__name__)
    # 当前签到的日期. 每日最多签到一次
    __cur_sign_date = None

    def __init__(self, client: MiniMir) -> None:
        super().__init__(client)
        # 间隔3分钟(180s)检查一次
        self._run_delay = 180

    def evaluate(self) -> bool:
        __date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        if self.__cur_sign_date == __date:
            return False
        p = self._player
        return not self.yield_wait_for() \
               and p.module_hj_completed and p.module_mj_completed \
               and p.module_yb_completed and p.module_fight_completed

    def execute(self) -> bool:
        resp = self.mir_req("user", "dayup")
        if resp is not None and "b" in resp and resp['b'] == 1:
            p = self._player
            __date = datetime.strftime(datetime.now(), "%Y-%m-%d")
            self.__cur_sign_date = __date
            # 重置各个模块的状态
            p.module_hj_completed = False
            p.module_yb_completed = False
            p.module_mj_completed = False
            p.module_fight_completed = False
            p.module_pk_completed = False
            self.__logger.info("=================== 签到成功:{} ====================".format(self.__cur_sign_date))
            pass
        else:
            self.__logger.info("=================== 今日已签到:{} ====================".format(self.__cur_sign_date))
            pass
        return False

    def __try_use_hj_item(self) -> bool:
        # 4. 使用幻境重置券
        if self._config.enable_use_hj_item:
            #  TODO: 未实现
            pass
        return

    def __lookup_item(self, item: int, amount: int):
        resp = self.mir_req("item", "loaditem")
        return
