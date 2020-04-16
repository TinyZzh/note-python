import logging
from dataclasses import dataclass
from datetime import datetime

from minimir import MiniMir
from minimir.GameAction import GameAction
from minimir.Utils import Utils


#   行会信息
@dataclass
class HangHuiInfo:
    guaji: int
    guajitime: datetime
    # 最后一次同步行会信息的时间
    time_last_refresh: datetime

    def __init__(self) -> None:
        super().__init__()


#
# Tick动作. _run_delay不生效.
#
class TickAction(GameAction):
    __logger = logging.getLogger(__name__)
    # 行会信息
    hh: HangHuiInfo = None

    def __init__(self, client: MiniMir) -> None:
        super().__init__(client)
        self._run_delay = -1

    def evaluate(self) -> bool:
        return True

    def execute(self) -> bool:
        # 行会挖矿
        self.__guild_ore()

        return False

    # 行会挖矿
    def __guild_ore(self):
        _now = datetime.now()
        # 半个小时检查一次挖矿情况
        if self.hh is None or ((_now - self.hh.time_last_refresh).seconds > 1800):
            self.hh = HangHuiInfo()
            self.hh.time_last_refresh = _now
            resp = self.mir_req("hh", "loadone")
            if resp is not None and "b" in resp and resp['b'] == 1:
                r = resp['hh']
                for fn, fv in r.items():
                    Utils.reflect_set_field([self.hh], fn, fv)
            pass
        if self.hh.guaji:
            duration = _now - self.hh.guajitime
            if duration.seconds >= self._config.max_wk_time:
                self.__logger.info("=================== 执行行会挖矿 =======================")
                # 结束挖矿
                resp = self.mir_req("hh", "loadone")
                # 开始挖矿
                resp = self.mir_req("hh", "loadone")
                self.auto_arrange_bag()
                pass
            pass
        return
