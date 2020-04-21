# -*- coding:UTF-8 -*-
import hashlib
import logging
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from queue import Queue

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
from minimir.Struct import AccountConfig
from minimir.TickAction import TickAction
from minimir.Utils import Utils
from minimir.YbAction import YbAction


class MiniMir:
    __logger = logging.getLogger(__name__)

    host = ""
    # 挂机设置
    setting: Setting

    actions = []

    _job_queue = Queue()

    def __init__(self, host: str, setting: Setting) -> None:
        self.host = host
        self.setting = setting
        super().__init__()

    # 登录游戏
    def login(self, _ac: AccountConfig):
        player = self.__user_load(_ac)
        self.actions.append(YbAction(self, player))
        self.actions.append(BattleAction(self, player))
        self.actions.append(CityAction(self, player))
        self.actions.append(TickAction(self, player))
        self.actions.append(SignInAction(self, player))
        return

    # 加载用户基础数据
    def __user_load(self, acc_config: AccountConfig) -> GamePlayer:
        __player = GamePlayer(self, acc_config)
        if acc_config is not None and acc_config.m_md5 is None:
            # TODO TINYZ. 未实现逻辑 - 秘钥混淆逻辑目前暂时还未破解
            _cur_timestamp = time.time()
            # val = md5(密码 + var + 时间戳)  => 123456d43228ea4953279321578cc6a4dc18f81586344509
            val = self.gen_md5(
                bytes("{}{}{}".format(acc_config.m_psw, self._base_secret, _cur_timestamp), "utf-8"))
            resp = __player.mir_request("account", "login", username=acc_config.m_user, password=acc_config.m_psw,
                                        val=val, var=self._base_secret,
                                        t=_cur_timestamp, without_md5=1)
            acc_config.m_md5 = resp['md5']
            pass

        __player.unit = BattleProperty()
        resp = __player.mir_request("user", "load", val=acc_config.m_val)
        if "user" in resp:
            u = resp["user"]
            for field_name, field_val in u.items():
                Utils.reflect_set_field([__player, __player.unit], field_name, field_val)
            pass
        else:
            raise Exception("获取用户数据失败.{}".format(resp))
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
        pass

    def _worker_main(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                job_func = self._job_queue.get(True)
                try:
                    executor.submit(job_func)
                except Exception as e:
                    logging.exception("job failure. action:[}".format(type(job_func)), e)
                finally:
                    self._job_queue.task_done()
                pass
            pass
        pass

    def gen_md5(self, data):
        hl = hashlib.md5()
        hl.update(data)
        return hl.hexdigest()
