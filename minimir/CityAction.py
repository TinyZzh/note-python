import logging
from datetime import datetime
from typing import List, Dict

from minimir import MiniMir, GamePlayer
from minimir.GameAction import GameAction


class CityAction(GameAction):
    __logger = logging.getLogger(__name__)
    # ============================== 城池争夺 ======================================
    # 当前占领的城市
    _cur_city_id: int = -1
    # 上一次检查城市的时间戳. 每间隔3分钟检查一次城池的状态
    _time_last_check: int = -1
    # 激活保护的时间. 超过1小时之后. 推出保护模式, 切换到正常的城池
    _time_active_protect: [datetime, None]

    def __init__(self, client: MiniMir, p: GamePlayer) -> None:
        super().__init__(client, p)
        self._run_delay = 180

    def evaluate(self) -> bool:
        return not self.yield_wait_for()

    def execute(self) -> bool:
        resp = self.mir_req("city", "load", time="")
        if resp['city']:
            _self_index = -1
            _dict = {}
            for _city_info in resp['city']:
                _dict[int(_city_info["cityid"])] = _city_info
                # 检查是否是自己占领
                if _city_info['userid'] != self._player.id:
                    _self_index = int(_city_info["cityid"])
                pass
            if _self_index > 0:
                # 检查是否需要退出保护模式
                if self._time_active_protect and (datetime.now() - self._time_active_protect).seconds > 3600:
                    self._time_active_protect = None
                    pass
                pass
            else:
                if self._cur_city_id > 0:
                    # 被攻击, 是否激活保护
                    self._time_active_protect = datetime.now() if self._config.enable_city_fuck_off_protect else None
                    pass
                pass
            # 设置city_id
            self._cur_city_id = _self_index
            # 查找城池
            _target_city_id = -1
            if self._config.custom_city_type > 0:
                _target_city_id = self._lookup_city([self._config.custom_city_type], _dict,
                                                    self._config.only_lookup_empty_city,
                                                    self._time_active_protect is not None)
                pass
            else:
                _target_city_id = self._lookup_city(self._config.city_type_weight_index, _dict,
                                                    self._config.only_lookup_empty_city,
                                                    self._time_active_protect is not None)
                pass
            if _target_city_id > 0:
                if _target_city_id != self._cur_city_id and self.mir_req_once("city", "pk", id=_target_city_id):
                    self._cur_city_id = _target_city_id
                    self.__logger.info("================= 占领城市:{} ================", _target_city_id)
                pass
            else:
                self.__logger.info("================= 未找到合适的城市 ================")
                pass
            return True
        else:
            return False

    def _lookup_city(self, city_type_list: List[int], city_dict: Dict[int, object],
                     lookup_empty_city: bool, fuck_off_protect: bool) -> int:
        """
        查找城池
        :param city_type_list:  查找的城池列表
        :param city_dict:   当前城池的占领信息
        :param lookup_empty_city:   只查找空城池
        :return: 可以占领的城池id
        """
        for ct in city_type_list:
            _city_offset_ary = range(7, 0, -1) if not fuck_off_protect else range(1, 8)
            _best_empty_city = -1
            for p_city_id_offset in _city_offset_ary:
                p_city_id = ct * 8 + p_city_id_offset
                if p_city_id not in city_dict and _best_empty_city < 0:
                    _best_empty_city = p_city_id

                if lookup_empty_city:
                    # 仅占领空城池模式
                    if p_city_id not in city_dict:
                        return p_city_id
                    pass
                else:
                    # TODO: 获取敌人的信息并对比自身的战斗力.

                    pass
                pass
            pass
        return -1
