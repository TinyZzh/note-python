import sys
import threading
import time
from queue import Queue

import requests
import schedule

# 游戏设置


_username = "wus1223"
_password = "godlike88115"
host = "http://mir.uuuyx.com/mir/game/do.php"
_account_md5 = "afe930611ceae9aa1cd4ece060750541"
# 当幻境结束时, 是否启用幻境重置卷
_enable_use_item_recovery_hj_lvl = True
# 使用祭坛重置幻境次数
_enable_jt_recovery_hj_lvl = False
# 幻境
_enable_hj_fight = True
# 推图boss战
_enable_fight_fight = True

# 游戏逻辑

_job_queue = Queue()

# 幻境等级
k_hj_lvl = 'hj_lvl'
k_fight_boss_lvl = 'fight_boss_lvl'
k_fight_boss_hp = 'boss_hp'
# 最小dps差距
k_min_of_dps = "min_of_dps"
# 押镖
k_yb = 'yb'
mir_datas = {
    "hj": 1,
    k_hj_lvl: 231,
    k_fight_boss_lvl: 17,
    k_fight_boss_hp: 9000,
    k_min_of_dps: 9999_9999,
    "guaji": 1,
    "boss": 1,
    k_yb: 1,
}


def _when_login():
    # _resp = mir_request("account", "login", username=_username, password=_password,
    #                     val="59e8c26c0494f7a19318b1a5a6a7e62f", var="6a4a4a74dcb2e74da312605575fe3d94",
    #                     t=int(time.time()), without_md5=1)
    # if _resp['b'] == 1 and int(_resp['account']['login']) > 0:
    #     pass

    # mir_request("shop", "holiday")
    # mir_request("user", "dayup")
    return


def _code_code():
    _resp = mir_request("code", "code", code="46B3EEC21ED5D4E379FD")
    if _resp['b'] != 1:
        pass
    print(_resp)
    pass


# 幻境战斗.
def _hj_fight():
    # print(mir_request("fight", "boss", id=6))
    # return
    cur_lvl = mir_datas[k_hj_lvl]
    if cur_lvl < 0:
        return
    _resp = mir_request("hj", "fight", id=cur_lvl)
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
        min_of_dps = mir_datas[k_min_of_dps] = min(mir_datas[k_min_of_dps],  (bhp / _rd) - (_td1 / _rd))
        print("level:{} battle:{}, 差:{}. p_dps:{}. boss dps:{}, round:{}, p_total_dmg:{}, boss_dmg:{}. pre_dps:{},"
              " min_of_dps:{}"
              .format(mir_datas[k_hj_lvl], result, bhp - _td1, _td1 / _rd, _td2 / _rd, _rd, _td1, _td2, (bhp / _rd),
                      min_of_dps))
        if is_win:
            mir_datas[k_hj_lvl] = cur_lvl + 1
            mir_datas[k_min_of_dps] = 9999_9999
    else:
        if str(_resp['t']).startswith("幻境战斗尚未结束"):
            # 接口调用太快. 战斗未结束. 等待下一个周期
            print("接口调用太频繁:{}".format(_resp))
            return
        # 无法再继续战斗了
        # 使用幻境重置卷
        # 使用祭坛重置
        if _jt_getcz():
            mir_datas[k_hj_lvl] = 1
            pass
        else:
            # 幻境接口调用次数耗尽
            mir_datas[k_hj_lvl] = -1
            pass
        print(_resp)
    return


# 祭坛重置 - 幻境进度和挑战次数重置
def _jt_getcz():
    if not _enable_jt_recovery_hj_lvl:
        return False
    _resp = mir_request("jt", "getczbl")
    if int(_resp['b']) != 1:
        _resp = mir_request("jt", "getcz")
    return int(_resp['b']) == 1


def _user_load():
    _resp = mir_request("user", "load", val="f237e41cd26b50b50bd0e75ac8d298a")

    return


def _item_itemku():
    _resp = mir_request("item", "itemku", id=74148011, type=2, ku=0)
    if _resp['b'] == 1:
        pass
    return


def _item_loaditem():
    _resp = mir_request("item", "loaditem", type=3, ku=0)
    if _resp['b'] == 1:
        pass
    return


def __lookup_item():
    return


def _user_talk():
    return


# 推图boss战
def _fight_fight():
    _resp = mir_request("fight", "fight", id=mir_datas[k_fight_boss_lvl])
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


# 押镖
def _ya():
    if mir_datas[k_yb] <= 0:
        return
    if 'yb_running' in mir_datas and int(mir_datas['yb_running']) == 1:
        mir_request("yb", "getitem")
        print("押镖结束. 领取奖励")
        pass

    _resp = mir_request("yb", "geti")
    if _resp['b'] == 1 and int(_resp['user']['yb_num']) > 0:
        mir_request("yb", "yb")
        mir_datas['yb_running'] = 1
        pass
    else:
        mir_datas[k_yb] = -1
        if 'yb_running' in mir_datas:
            del mir_datas['yb_running']
        pass
    return


def _phb_phb():
    if _account_md5 is not None or len(_account_md5) > 0:
        _resp = mir_request("phb", "phb", time=int(time.time()), type=10)
    return


# 工具逻辑

def _worker_main():
    while 1:
        job_func = _job_queue.get()
        job_func()
        _job_queue.task_done()
    pass


def _start():
    # hashlib.md5().hexdigest()
    # _code_code()

    _when_login()
    #   定时任务
    if _enable_fight_fight:
        schedule.every(2).seconds.do(_job_queue.put, _fight_fight)
    elif _enable_hj_fight:
        schedule.every(3).seconds.do(_job_queue.put, _hj_fight)

    # schedule.every(10).seconds.do(_job_queue.put, _phb_phb)
    schedule.every(100).seconds.do(_job_queue.put, _ya)
    #  启动工作线程
    worker_thread = threading.Thread(target=_worker_main)
    worker_thread.start()
    while True:
        schedule.run_pending()
        time.sleep(1)
    return


def mir_request(module, action, **kargs):
    _params = {}
    _params = kargs if kargs is not None else {}
    _params["m"] = module
    _params["a"] = action
    if "without_md5" in kargs:
        del _params["without_md5"]
    else:
        _params["md5"] = _account_md5
        pass

    _url_extra = []
    for k, v in kargs.items():
        _url_extra.append("{}={}".format(k, v))
        pass

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
        "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd."
                  "ms-excel, application/vnd.ms-powerpoint, application/msword, */*"
    }
    print("[request] module:{}, action:{}, kargs:{}".format(module, action, kargs))
    r = requests.post("{}?{}".format(host, "&".join(_url_extra)), data=_params, headers=headers)
    if r.status_code == requests.codes.ok:
        resp = r.json()
        # if resp['b'] != 1:
        #     print(resp)
        return resp
    else:
        r.raise_for_status()
    pass


if __name__ == '__main__':
    sys.exit(_start())
