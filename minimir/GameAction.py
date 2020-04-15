# -*- coding:UTF-8 -*-
import time

from minimir import MiniMir
from minimir.GamePlayer import GamePlayer


class GameAction:
    # 客户端
    _m_client: MiniMir = None
    # 用户信息
    _player: GamePlayer

    # 间隔执行. 避免太频繁的调用接口
    _last_run_timestamp = -1
    _run_delay = -1

    def __init__(self, client: MiniMir) -> None:
        self._m_client = client
        super().__init__()
        self._player = client.player

    def evaluate(self) -> bool:
        raise NotImplementedError("unimplemented method:evaluate()")

    def execute(self) -> bool:
        raise NotImplementedError("unimplemented method:execute()")

    def client(self) -> MiniMir:
        return self._m_client

    def mir_req(self, module, action, **kargs):
        return self.client().mir_request(module, action, **kargs)

    #
    def try_yield_run(self) -> bool:
        if self._run_delay <= 0:
            return True
        _timestamp = time.time()
        if _timestamp - self._last_run_timestamp >= self._run_delay:
            self._last_run_timestamp = _timestamp
            return True
        else:
            return False
