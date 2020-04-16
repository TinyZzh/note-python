# -*- coding:UTF-8 -*-
import hashlib
import logging
import threading
import time
from datetime import datetime
from queue import Queue

import requests
import schedule

#
# m=account&a=login&username=zou90512&password=123456&val=36619668b04d661de0ba6bc7d6fa7ecb&var=d43228ea4953279321578cc6a4dc18f8&t=1586339079
#
from minimir.BattleAction import BattleAction
from minimir.CityAction import CityAction
from minimir.GameAction import GameAction
from minimir.GamePlayer import GamePlayer, BattleProperty
from minimir.Setting import Setting
from minimir.SignInAction import SignInAction
from minimir.TickAction import TickAction
from minimir.Utils import Utils
from minimir.YbAction import YbAction


class MiniMir:
    __logger = logging.getLogger(__name__)

    # md5(1079296108 + BFEBFBFF + 000306C3)  => d43228ea4953279321578cc6a4dc18f8
    _base_secret = 'd43228ea4953279321578cc6a4dc18f8'

    _host = ""
    # 登录之后获取
    _account_md5 = None
    _account_val = None
    player: GamePlayer
    # 挂机设置
    setting: Setting

    actions = []

    _job_queue = Queue()

    def __init__(self, host, md5: str = None, val: str = None) -> None:
        self._host = host
        self._account_md5 = md5
        self._account_val = val
        super().__init__()
        self.setting = Setting()
        self.setting.load_setting()

    # 登录游戏
    def login(self, user, psw):
        if self._account_md5 is None:
            # TODO 未实现逻辑 - 秘钥混淆逻辑目前暂时还未破解
            _cur_timestamp = time.time()
            # val = md5(密码 + var + 时间戳)  => 123456d43228ea4953279321578cc6a4dc18f81586344509
            val = self.gen_md5(bytes("{}{}{}".format(psw, self._base_secret, _cur_timestamp), "utf-8"))
            resp = self.mir_request("account", "login", username=user, password=psw,
                                    val=val, var=self._base_secret,
                                    t=_cur_timestamp, without_md5=1)
            self._account_md5 = resp['md5']
            pass
        self.player = self.__user_load()

        self.actions.append(YbAction(self))
        self.actions.append(BattleAction(self))
        self.actions.append(CityAction(self))
        self.actions.append(TickAction(self))
        self.actions.append(SignInAction(self))

        self.start_logic_tick()
        return

    # 加载用户基础数据
    def __user_load(self) -> GamePlayer:
        __player = GamePlayer()
        __player.unit = BattleProperty()
        resp = self.mir_request("user", "load", val=self._account_val)
        if "user" in resp:
            u = resp["user"]
            for field_name, field_val in u.items():
                Utils.reflect_set_field([__player, __player.unit], field_name, field_val)
            pass
        else:
            raise Exception("获取用户数据失败.")
        return __player



    # 逻辑心跳
    def tick(self):
        for action in self.actions:
            try:
                if isinstance(action, GameAction) and action.evaluate():
                    ___now___ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.__logger.debug("action:{} start:{}".format(___now___, type(action)))
                    action.execute()
            except Exception as e:
                self.__logger.exception(e)
            pass
        return

    # 开启逻辑
    def start_logic_tick(self):
        #   定时任务
        schedule.every(1).seconds.do(self._job_queue.put, self.tick)
        #  启动工作线程
        worker_thread = threading.Thread(target=self._worker_main)
        worker_thread.start()
        while True:
            schedule.run_pending()
            time.sleep(1)
        return

    def _worker_main(self):
        while 1:
            job_func = self._job_queue.get()
            job_func()
            self._job_queue.task_done()
        pass

    # 调用接口
    def mir_request(self, module, action, **kargs):
        _params = {}
        _params = kargs if kargs is not None else {}
        _params["m"] = module
        _params["a"] = action
        if "without_md5" in kargs:
            del _params["without_md5"]
        else:
            _params["md5"] = self._account_md5
            pass

        _url_extra = []
        for k, v in kargs.items():
            _url_extra.append("{}={}".format(k, v))
            pass

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
            "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, "
                      "application/vnd."
                      "ms-excel, application/vnd.ms-powerpoint, application/msword, */*"
        }
        # 简单的伪造IP   - hping3伪造源IP   - REMOTE_ADDR
        if self.setting.enable_random_client_ip:
            headers["CLIENT-IP"] = self.setting.tmp_url_header_local_ip
            headers["X-FORWARDED-FOR"] = self.setting.tmp_url_header_local_ip
            headers["X-REAL-IP"] = self.setting.tmp_url_header_local_ip
            pass
        self.__logger.debug("[request] module:{}, action:{}, kargs:{}".format(module, action, kargs))
        r = requests.post("{}?{}".format(self._host, "&".join(_url_extra)), data=_params, headers=headers)
        if r.status_code == requests.codes.ok:
            resp = r.json()
            # if resp['b'] != 1:
            #     self.__logger.debug(resp)
            return resp
        else:
            r.raise_for_status()
        return

    def gen_md5(self, data):
        hl = hashlib.md5()
        hl.update(data)
        return hl.hexdigest()
