import logging
from dataclasses import dataclass
from datetime import datetime

from minimir import MiniMir, GamePlayer
from minimir.GameAction import GameAction
from minimir.Utils import Utils


#   行会信息
@dataclass
class HangHuiInfo:
    guaji: int
    guajitime: datetime
    # 最后一次同步行会信息的时间
    time_last_refresh: datetime
    # 是否有行会
    has_hh: bool

    def __init__(self) -> None:
        super().__init__()
        self.guaji = 0


#
# Tick动作. _run_delay不生效.
#
class TickAction(GameAction):
    __logger = logging.getLogger(__name__)
    # 行会信息
    hh: HangHuiInfo = None

    def __init__(self, client: MiniMir, p: GamePlayer) -> None:
        super().__init__(client, p)
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
            resp = self.mir_req("hh", "loadone")
            if resp is not None and "b" in resp and resp['b'] == 1:
                self.hh = HangHuiInfo()
                if 'hh' in resp:
                    self.hh.has_hh = True
                    r = resp['hh']
                    for fn, fv in r.items():
                        Utils.reflect_set_field([self.hh], fn, fv)
                        pass
                    # TODO：刚进入行会首次需要开始挂机
                    self.mir_req("hh", "guaji")
                    pass
                else:
                    self.hh.has_hh = False
                    self.hh.guaji = False
                    pass
                self.hh.time_last_refresh = _now
            pass
        if self.hh is None or not self.hh.has_hh:
            return
        if self.hh.guaji:
            duration = _now - self.hh.guajitime
            if duration.seconds >= self._config.max_wk_time:
                self.__logger.info("=================== 执行行会挖矿 =======================")
                # 结束挖矿. type为挖矿倍率
                resp = self.mir_req("hh", "guajioff", type=1)
                # 开始挖矿
                resp = self.mir_req("hh", "guaji")
                self.auto_arrange_bag()
                pass
            pass
        return