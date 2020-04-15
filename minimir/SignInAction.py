import time
from datetime import datetime

from minimir import MiniMir
from minimir.GameAction import GameAction


#
# 每日签到
#
class SignInAction(GameAction):
    # 当前签到的日期. 每日最多签到一次
    __cur_sign_date = None

    def __init__(self, client: MiniMir) -> None:
        super().__init__(client)
        # 间隔3分钟检查一次
        self._run_delay = 1

    def evaluate(self) -> bool:
        __date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        if self.__cur_sign_date == __date:
            return False
        p = self._player
        return self.try_yield_run() \
               and p.module_hj_completed and p.module_mj_completed \
               and p.module_yb_completed and p.module_fight_completed \
               and p.module_pk_completed

    def execute(self) -> bool:
        resp = self.mir_req("city", "pk")
        if resp['b'] == 1:
            p = self._player
            __date = datetime.fromtimestamp(time.time()).isoformat("YYYY-MM-DD")
            self.__cur_sign_date = __date
            # 重置各个模块的状态
            p.module_hj_completed = False
            p.module_yb_completed = False
            p.module_mj_completed = False
            p.module_fight_completed = False
            p.module_pk_completed = False
        return False
