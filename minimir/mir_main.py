import logging

from minimir.MiniMir import MiniMir

if __name__ == "__main__":
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    __logger_handlers = [
        logging.FileHandler(encoding='utf-8', mode='a', filename='./run.log'),
        logging.StreamHandler()
    ]
    logging.basicConfig(handlers=__logger_handlers, level='INFO', datefmt="[%Y-%m-%d %H:%M:%S]", format=log_format)
    logging.getLogger('schedule').level = logging.WARNING

    game = MiniMir(host="http://mir.uuuyx.com/mir/game/do.php", md5="6f549dc3fcd5df3465418315464a417a",
                   val="837f7263192c4f850e0a74f5a98f59ca")
    game.login("wus1223", "godlike88115")
    pass
