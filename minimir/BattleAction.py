# -*- coding:UTF-8 -*-
import sys

from minimir.GameAction import GameAction


class BattleAction(GameAction):
    # 挂机
    # 挂机BOSS
    # BOSS之家
    # 密境

    # 幻境
    _hj_lvl = 1,
    # 是否允许使用幻境重置券重置幻境
    _allow_use_hj_item = False

    _k_min_of_dps = sys.maxsize
    # 是否战斗中
    _is_battle = False

    # 推图Boss的ID
    __fight_fight_id = 18

    def evaluate(self) -> bool:

        return True

    def execute(self) -> bool:

        return False

    # 幻境战斗.
    def __fight_fight(self):
        _resp = self.mir_req("fight", "fight", id=self.__fight_fight_id)
        if _resp['b'] == 1:
            _td1 = 0
            _td2 = 0
            _rd = float(_resp['fight']['num'])
            for __info in _resp['fight']['process']:
                _d = str.split(__info, "|")
                if int(_d[0]) == 1:
                    _td1 += int(_d[1])
                else:
                    _td2 += int(_d[1])
                pass
            is_win = int(_resp['fight']['result']) == 1
            res = "胜利" if is_win else "失败"
            left = mir_datas[k_fight_boss_hp] - _td1
            # 预测dps
            r_dps = mir_datas[k_fight_boss_hp] / _rd
            # 玩家实际dps
            p_dps = _td1 / _rd
            # boss的dps
            b_dps = _td2 / _rd
            # 预测胜利的dps和玩家实际dps的差值. 小于0说明战斗成功
            # 预判大概要提升多少战斗力才能获胜
            of_dps = r_dps - p_dps
            min_of_dps = mir_datas[k_min_of_dps] = min(mir_datas[k_min_of_dps], of_dps)
            print("level:{} battle:{}. p_dps:{}. boss_dps:{}, round:{}, p_total_dmg:{}, boss_dmg:{},"
                  " left:{}, 预测dps:{}, of_dps:{}, min:{}"
                  .format(mir_datas[k_hj_lvl], res, p_dps, b_dps, _rd, _td1, _td2, left, r_dps, of_dps, min_of_dps))
        else:
            if not str(_resp['t']).startswith("BOSS战斗尚未结束"):
                print(_resp)
            pass
        return

    def _hj_fight(self):
        # print(mir_request("fight", "boss", id=6))
        # return
        cur_lvl = self._hj_lvl
        if cur_lvl < 0:
            return
        _resp = self.mir_req("hj", "fight", id=cur_lvl)
        if _resp['b'] == 1:
            _td1 = 0
            _td2 = 0
            _rd = float(_resp['fight']['num'])
            for __info in _resp['fight']['process']:
                _d = str.split(__info, "|")
                if int(_d[0]) == 1:
                    _td1 += int(_d[1])
                else:
                    _td2 += int(_d[1])
                pass
            is_win = int(_resp['fight']['result']) == 1
            bhp = _resp['fight']['bhp']
            result = "胜利" if is_win else "失败"
            min_of_dps = self._k_min_of_dps = min(self._k_min_of_dps, (bhp / _rd) - (_td1 / _rd))
            print("level:{} battle:{}, 差:{}. p_dps:{}. boss dps:{}, round:{}, p_total_dmg:{}, boss_dmg:{}. pre_dps:{},"
                  " min_of_dps:{}"
                  .format(self._hj_lvl, result, bhp - _td1, _td1 / _rd, _td2 / _rd, _rd, _td1, _td2, (bhp / _rd),
                          min_of_dps))
            if is_win:
                self._hj_lvl = cur_lvl + 1
                self._k_min_of_dps = sys.maxsize
        else:
            if str(_resp['t']).startswith("幻境战斗尚未结束"):
                # 接口调用太快. 战斗未结束. 等待下一个周期
                print("接口调用太频繁:{}".format(_resp))
                return
            # 无法再继续战斗了
            # 使用幻境重置卷
            # 使用祭坛重置
            if _jt_getcz():
                self._hj_lvl = 1
                pass
            else:
                # 幻境接口调用次数耗尽
                self._hj_lvl = -1
                pass
            print(_resp)
        return

    # 幻境战斗.
    def __mj_fight(self):

        return
