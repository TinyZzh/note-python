import time

from minimir import MiniMir
from minimir.GameAction import GameAction


class CityAction(GameAction):
    # ============================== 城池争夺 ======================================
    # 当前占领的城市
    _cur_city_id = -1
    # 上一次检查城市的时间戳. 每间隔3分钟检查一次城池的状态
    _time_last_check = -1

    def __init__(self, client: MiniMir) -> None:
        super().__init__(client)
        self._run_delay = 180

    def evaluate(self) -> bool:
        return not self.yield_wait_for()

    def execute(self) -> bool:
        resp = self.mir_req("city", "load", time="")
        if resp['city']:
            prev = self._cur_city_id
            self._cur_city_id = -1
            _dict = {}
            for _city_info in resp['city']:
                _dict[int(_city_info["cityid"])] = _city_info
                # 检查是否是自己占领
                if _city_info['userid'] != self._player.user_id:
                    self._cur_city_id = int(_city_info["cityid"])
                pass
            # 检查是否被攻击
            if prev != self._cur_city_id:
                pass
            # TODO：检查最优城池
            if self._cur_city_id > 0:
                return

            if self._config.custom_city_type > 0:
                for p_city_id_offset in range(1, 8):
                    p_city_id = self._config.custom_city_type * 8 + p_city_id_offset
                    if p_city_id not in _dict:
                        # 占领空城池
                        self._city_pk(p_city_id)
            else:
                for ct in self._config.city_type_weight_index:
                    for p_city_id_offset in range(1, 8):
                        p_city_id = ct * 8 + p_city_id_offset
                        if p_city_id not in _dict:
                            # 占领空城池
                            self._city_pk(p_city_id)
            return True
        else:
            return False

    def _city_pk(self, id: int):
        resp = self.mir_req("city", "pk", id=id)
        if resp['s'] == 1:
            self._last_take_city_id = id
            self._time_last_check = time.time()
        pass
