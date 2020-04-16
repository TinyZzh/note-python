# -*- coding:UTF-8 -*-
import logging
import math
import sys

from minimir.GameAction import GameAction


# 挂机
# 挂机BOSS
# BOSS之家
# 密境
class BattleAction(GameAction):
    __logger = logging.getLogger(__name__)
    # ================================ 战报相关 ==============================
    __f_min_of_dps = sys.maxsize
    # 是否战斗中
    __is_battle = False
    # 推图BOSS战, 连续失败次数
    __fight_fail_count = 0

    def evaluate(self) -> bool:
        if self.yield_wait_for():
            return False
        return not self._player.module_hj_completed \
               or not self._player.module_mj_completed \
               or not self._player.module_fight_completed

    def execute(self) -> bool:
        # 幻境 - 秘境 - 推图BOSS - PK -
        if not self._player.module_hj_completed:
            self.__hj_fight()
        elif not self._player.module_mj_completed:
            self.__mj_fight()
        elif not self._player.module_fight_completed:
            self.__fight_fight()
        return True

    # 幻境战斗
    def __hj_fight(self):
        if self._player.hj_num <= 0:
            # 尝试祭坛重置幻境
            if not self.__try_reset_hj():
                self._player.module_hj_completed = True
                self.__reset_min_of_dps()
                self._run_delay = -1
                self.__logger.info("=========================== 幻境结束 ============================================")
            return
        _target_hj_lvl = self._player.hj_lvl + 1
        _resp = self.mir_req("hj", "fight", id=_target_hj_lvl)
        if _resp['b'] == 1:
            _td1 = 0
            _td2 = 0
            _rd = float(_resp['fight']['num'])
            # 10回合 = 1秒CD
            self._run_delay = math.ceil(_rd / self._config.each_second_delay_of_rounds)
            for __info in _resp['fight']['process']:
                _d = str.split(__info, "|")
                if int(_d[0]) == 1:
                    _td1 += int(_d[1])
                else:
                    _td2 += int(_d[1])
                pass
            is_win = int(_resp['fight']['result']) == 1
            bhp = _resp['fight']['bhp']
            result = "胜利" if is_win else "LOSE"
            min_of_dps = self.__f_min_of_dps = min(self.__f_min_of_dps, (bhp / _rd) - (_td1 / _rd))
            self.__logger.info("hj_id:{}.{}, 差:{}. p_dps:{:.2f}. boss dps:{:.2f}, round:{:n}, ptd:{:.2f}, btd:{:.2f}."
                               "pre_dps:{:.2f}, min_of_dps:{:.2f}"
                               .format(self._player.hj_lvl, result, bhp - _td1, _td1 / _rd, _td2 / _rd, _rd, _td1, _td2,
                                       (bhp / _rd), min_of_dps))
            # 扣除幻境挑战次数
            self._player.hj_num -= 1
            if is_win:
                self._player.hj_lvl += 1
                self.__reset_min_of_dps()
        elif str(_resp['t']).startswith("幻境战斗尚未结束"):
            pass
        else:
            self.__logger.info(_resp)
        return

    # 秘境战斗.
    def __mj_fight(self):
        # TODO: 未实现
        if self._player.mj_num <= 0:
            self._player.module_mj_completed = True
            self.__reset_min_of_dps()
            self._run_delay = -1
            self.__logger.info("=========================== 密境结束 ============================================")
            return
        __target_mj_lvl = self._player.mj_lvl + 1
        _resp = self.mir_req("mj", "fight", id=__target_mj_lvl)
        if _resp['b'] == 1:
            # player total damage
            _ptd = 0
            # boss total damage
            _btd = 0
            _rd = float(_resp['fight']['num'])
            # 10回合 = 1秒CD
            self._run_delay = math.ceil(_rd / self._config.each_second_delay_of_rounds)
            for __info in _resp['fight']['process']:
                _d = str.split(__info, "|")
                if int(_d[0]) == 1:
                    _ptd += int(_d[1])
                else:
                    _btd += int(_d[1])
                pass
            is_win = int(_resp['fight']['result']) == 1
            bhp = _resp['fight']['bhp']
            result = "胜利" if is_win else "LOSE"
            min_of_dps = self.__f_min_of_dps = min(self.__f_min_of_dps, (bhp / _rd) - (_ptd / _rd))
            self.__logger.info("mj_id:{}.{}, 差:{}. p_dps:{:.2f}. boss dps:{:.2f}, round:{:.n}, ptd:{:.2f}, btd:{:.2f}."
                               "pre_dps:{:.2f}, min_of_dps:{:.2f}"
                               .format(self._player.mj_lvl, result, bhp - _ptd, _ptd / _rd, _btd / _rd, _rd, _ptd, _btd,
                                       (bhp / _rd), min_of_dps))
            # 扣除秘境挑战次数
            self._player.mj_num -= 1
            if is_win:
                self._player.mj_lvl += 1
                self.__reset_min_of_dps()
        elif str(_resp['t']).startswith("秘境战斗尚未结束"):
            self.__logger.info(_resp)
            pass
        elif str(_resp['t']).startswith("巅峰后才可以挑战"):
            self._player.module_mj_completed = True
            self.__logger.info(_resp)
        else:
            self.__logger.info(_resp)
        return

    # VIP扫荡推图BOSS特权
    def __fight_fight_vip(self):
        return

    # 推图BOSS战斗. - 优先级最低. 尝试100次战斗, 战斗结果都是失败则说明战斗力不足
    def __fight_fight(self):
        if self._player.mapboss <= 0:
            if self._config.enable_use_boss_item:
                # TODO: 自动使用BOSS挑战券增加挑战次数
                pass
            else:
                self.__fight_fail_count = self._config.fight_fight_fail_threshold
                pass
        if self.__fight_fail_count >= self._config.fight_fight_fail_threshold:
            self._player.module_fight_completed = True
            self._run_delay = -1
            self.__logger.info("=========================== 推图BOSS结束 ============================================")
            self.mir_req("fight", "guaji", id=self._player.map)
            return
        # 挑战下一张地图
        __target_map = self._player.map + 1
        _resp = self.mir_req("fight", "fight", id=__target_map)
        if _resp['b'] == 1:
            __fi = _resp['fight']
            # 战斗回合数
            _rd = float(__fi['num'])
            # 10回合 = 1秒CD
            self._run_delay = math.ceil(_rd / self._config.each_second_delay_of_rounds)
            _td1 = 0
            _td2 = 0
            for __info in __fi['process']:
                _d = str.split(__info, "|")
                if int(_d[0]) == 1:
                    _td1 += int(_d[1])
                else:
                    _td2 += int(_d[1])
                pass
            is_win = int(_resp['fight']['result']) == 1
            if is_win:
                self._player.map += 1
                self._player.mapboss -= 1
                self.__fight_fail_count = 0
            else:
                self.__fight_fail_count += 1
                pass
            res = "胜利" if is_win else "lose"
            p_dps = _td1 / _rd
            b_dps = _td2 / _rd
            self.__logger.info("map:{} - {}. p_dps:{:.2f}. boss_dps:{:.2f}, 回合数:{:n}, ptd:{:.2f}, btd:{:.2f}"
                               .format(__target_map, res, p_dps, b_dps, _rd, _td1, _td2))
            pass
        elif str(_resp['t']).startswith("当前状态不可以挑战BOSS，请先取消挂机"):
            self.mir_req("fight", "guajioff")
            self.__logger.debug(_resp)
            pass
        elif str(_resp['t']).startswith("挑战BOSS剩余次数不足"):
            if self._config.enable_use_boss_item:
                # self.mir_req("fight", "guajioff")
                # TODO: 使用boss挑战卷道具增加次数
                pass
            self.__fight_fail_count = self._config.fight_fight_fail_threshold
            self.__logger.debug(_resp)
        elif str(_resp['t']).startswith("转生太低"):
            # 无法挑战. 直接结束
            self.__fight_fail_count = self._config.fight_fight_fail_threshold
            self.__logger.debug(_resp)
        elif str(_resp['t']).startswith("BOSS战斗尚未结束"):
            self.__logger.info(_resp)
            pass
        else:
            self.__logger.info(_resp)
            pass
        return

    # 尝试重置幻境
    def __try_reset_hj(self) -> bool:
        # 1. 重置昨日
        _resp = self.mir_req("jt", "getczbl")
        if str(_resp['t']).startswith("昨日已经领取过重置了"):
            # 2. 重置今日
            _resp = self.mir_req("jt", "getcz")
            if str(_resp['t']).startswith("今天已经领取过重置了"):
                # 3. 使用祭坛进度重置
                if self._config.enable_use_jt_exp:
                    _resp = self.mir_req("jt", "load")
                    if int(_resp['b']) == 1:
                        if int(_resp['jt']['jt_exp']) >= 1000:
                            _resp = self.mir_req("jt", "buy")
                            if int(_resp['b']) == 1:
                                self.__hj_reset()
                                return True
                    pass
                pass
            else:
                self.__hj_reset()
                return True
        else:
            self.__hj_reset()
            return True
        return False

    def __hj_reset(self):
        self._player.hj_lvl = 0
        self._player.hj_num = 1000
        self.__logger.info("======================== 幻境重置成功 ==============================")
        return

    def __mj_reset(self):
        self._player.mj_lvl = 0
        self._player.mj_num = 1000
        self.__logger.info("======================== 秘境重置成功 ==============================")
        return

    def __reset_min_of_dps(self):
        self.__f_min_of_dps = sys.maxsize
        return
