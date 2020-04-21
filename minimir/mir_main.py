# -*- coding:UTF-8 -*-

if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()

    import logging
    from minimir.MiniMir import MiniMir
    from minimir.Setting import Setting

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    __logger_handlers = [
        logging.FileHandler(encoding='utf-8', mode='a', filename='./run.log'),
        logging.StreamHandler()
    ]
    logging.basicConfig(handlers=__logger_handlers, level='DEBUG', datefmt="[%Y-%m-%d %H:%M:%S]", format=log_format)
    logging.getLogger('schedule').level = logging.WARNING

    try:
        _setting = Setting()
        _accounts = _setting.load_setting()

        game = MiniMir(host="http://mir.uuuyx.com/mir/game/do.php", setting=_setting)
        for _ac in _accounts:
            try:
                game.login(_ac)
            except Exception as e:
                logging.exception("ac:{} login failure.".format(_ac), e)
            pass
        game.start_logic_tick()
    except Exception as e:
        logging.exception(e)
    pass
