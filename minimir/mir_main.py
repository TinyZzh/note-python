# -*- coding:UTF-8 -*-
from minimir.Utils import Utils

if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()

    import logging
    from minimir.MiniMir import MiniMir

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    __logger_handlers = [
        logging.FileHandler(encoding='utf-8', mode='a', filename='./run.log'),
        logging.StreamHandler()
    ]
    logging.basicConfig(handlers=__logger_handlers, level='DEBUG', datefmt="[%Y-%m-%d %H:%M:%S]", format=log_format)
    logging.getLogger('schedule').level = logging.WARNING

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
