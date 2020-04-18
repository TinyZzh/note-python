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

    game = MiniMir(host="http://mir.uuuyx.com/mir/game/do.php", md5="1e7b0a0526b4cc9ca288e4b14ce21a3f",
                   val="8dbaa6fa781f35975f6c4e9baf630698")
    game.login("wus1223", "godlike88115")
    pass
