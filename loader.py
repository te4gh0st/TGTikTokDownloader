import platform

from aiogram import Bot
from aiogram import Dispatcher
from loguru import logger

from config import *

load_dotenv()
logger.add('tgTicTikDown.log', level='INFO', rotation='10 MB', compression='zip')

bt = Bot(TOKEN)
dp = Dispatcher(bt)


def debug_run() -> bool:
    """
    Проверка OS.
    :rtype: True if system is Linux.
    """
    if platform.system() == 'Linux':
        return False
    else:
        logger.debug('Запущено в режиме отладки')
        return True


def run_mode():
    if WEBHOOK_ACTIVE == '0':
        return False
    elif WEBHOOK_ACTIVE == '1':
        return True
    else:
        logger.critical('WEBHOOK_ACTIVE INCORRECT!')
        exit()
