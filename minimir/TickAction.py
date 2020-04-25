import logging
from datetime import datetime

from minimir import MiniMir, GamePlayer
from minimir.GameAction import GameAction
from minimir.Setting import Setting
from minimir.Struct import HangHuiInfo
from minimir.Utils import Utils


#
# Tick动作. _run_delay不生效.
#
class TickAction(GameAction):
    __logger = logging.getLogger(__name__)

    def __init__(self, client: MiniMir, p: GamePlayer, setting: Setting) -> None:
        super().__init__(client, p, setting)
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
        _hh_ = self._player.hh if hasattr(self._player, "hh") else None
        # 半个小时检查一次挖矿情况
        if _hh_ is None or ((_now - _hh_.time_last_refresh).seconds > 600):
            resp = self.mir_req_once("hh", "loadone", feedback=lambda x: self.auto_arrange_bag())
            if resp:
                _hh_ = HangHuiInfo()
                if 'hh' in resp:
                    _hh_.has_hh = True
                    r = resp['hh']
                    for fn, fv in r.items():
                        Utils.reflect_set_field([_hh_], fn, fv)
                        pass
                    # 刚进入行会首次需要开始挂机
                    self.mir_req_once("hh", "guaji")
                    pass
                else:
                    _hh_.has_hh = False
                    _hh_.guaji = False
                    pass
                _hh_.time_last_refresh = _now
                # 完成行会信息的同步
                self._player.hh = _hh_
            pass
        if _hh_ is None or not _hh_.has_hh:
            return
        if _hh_.guaji:
            duration = _now - _hh_.guajitime
            if duration.seconds >= self._config.max_wk_time:
                self.__logger.info("=================== 执行行会挖矿 =======================")
                # 结束挖矿. type为挖矿倍率
                if self.mir_req_once("hh", "guajioff", type=1):
                    _hh_.guaji = 0
                    # 开始挖矿
                    if self.mir_req_once("hh", "guaji", feedback=lambda x: self.auto_arrange_bag()):
                        _hh_.guaji = 1
                        _hh_.guajitime = _now
                        pass
                    pass
                pass
            pass
        return
