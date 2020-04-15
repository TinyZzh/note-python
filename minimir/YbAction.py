import time

from minimir import MiniMir
from minimir.GameAction import GameAction


# 押镖
class YbAction(GameAction):
    # 是否正在押镖
    _is_running = False

    def __init__(self, client: MiniMir) -> None:
        super().__init__(client)
        self._run_delay = 100

    def evaluate(self) -> bool:
        if self._is_running:
            return self.try_yield_run()
        else:
            # 非押镖状态. 每次Tick检查一次
            return not self._player.module_yb_completed

    def execute(self) -> bool:
        if self._is_running:
            self.mir_req("yb", "getitem")
            print("============== 押镖结束. 领取奖励 ======================")
            self._run_delay = -1
            pass

        _resp = self.mir_req("yb", "geti")
        if _resp['b'] == 1:
            self._player.module_yb_completed = int(_resp['user']['yb_num']) <= 0
            if not self._player.module_yb_completed:
                _resp2 = self.mir_req("yb", "yb")
                self._is_running = True
                # 押镖耗时100秒
                self._run_delay = 100
            else:
                self._is_running = False
                pass
        return True
