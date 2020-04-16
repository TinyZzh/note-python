# -*- coding:UTF-8 -*-
import logging
import time

from minimir import MiniMir, Setting
from minimir.GamePlayer import GamePlayer


class GameAction:
    __logger = logging.getLogger(__name__)
    # 客户端
    _m_client: MiniMir
    # 用户信息
    _player: GamePlayer
    # 挂机设置
    _config: Setting

    # 间隔执行. 避免太频繁的调用接口
    _last_run_timestamp = -1
    _run_delay = -1

    def __init__(self, client: MiniMir) -> None:
        super().__init__()
        self._m_client = client
        self._player = client.player
        self._config = client.setting

    def evaluate(self) -> bool:
        raise NotImplementedError("unimplemented method:evaluate()")

    def execute(self) -> bool:
        raise NotImplementedError("unimplemented method:execute()")

    def client(self) -> MiniMir:
        return self._m_client

    def mir_req(self, module, action, **kargs):
        return self.client().mir_request(module, action, **kargs)

    #
    #   是否需要等待一段时间?
    #
    def yield_wait_for(self) -> bool:
        if self._run_delay <= 0:
            return False
        _timestamp = time.time()
        __offset = _timestamp - self._last_run_timestamp
        if __offset >= self._run_delay:
            self.__logger.debug("--------------------- {}, {} ------------------------".format(type(self), __offset))
            self._last_run_timestamp = _timestamp
            return False
        else:
            return True
