import logging

from minimir.MiniMir import MiniMir

if __name__ == "__main__":
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    __logger_handlers = [
        logging.FileHandler(encoding='utf-8', mode='a', filename='./run.log'),
        logging.StreamHandler()
    ]
    logging.basicConfig(handlers=__logger_handlers, level='DEBUG', datefmt="[%Y-%m-%d %H:%M:%S]", format=log_format)
    logging.getLogger('schedule').level = logging.WARNING

    game = MiniMir(host="http://mir.uuuyx.com/mir/game/do.php", md5="f9acb93a61716a49f34c720bbdb04a22",
                   val="8c8338c1363ed9143cb1be2eb99b5ed4")
    game.login("wus1223", "godlike88115")
    pass
