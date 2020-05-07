# -*- coding:UTF-8 -*-
from logging import handlers

from minimir.Utils import Utils


def __init_logging_config() -> None:
    import logging
    log_format = "%(asctime)s[%(levelname)s] - %(name)s[%(funcName)s:%(lineno)d]: %(message)s"
    _fl = handlers.TimedRotatingFileHandler(filename="./logs/run.log", when='D', interval=1, backupCount=5,
                                            encoding='utf-8')
    _fl.setLevel(logging.DEBUG)
    _sl = logging.StreamHandler()
    _sl.setLevel(logging.INFO)
    logging.basicConfig(handlers=[_fl, _sl], level='DEBUG', datefmt="[%Y-%m-%d %H:%M:%S]", format=log_format)
    logging.getLogger('schedule').level = logging.WARNING
    return


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()

    import logging
    from minimir.MiniMir import MiniMir

    __init_logging_config()

    try:
        game = MiniMir(host="http://mir.uuuyx.com/mir/game/do.php")
        _accounts = Utils.load_account_setting()
        for _ac in _accounts:
            try:
                game.login(_ac)
            except Exception as e:
                logging.exception("ac:{} login failure.".format(str(_ac)), e)
            pass
        game.start_logic_tick()
    except Exception as e:
        logging.exception(e)
    pass
