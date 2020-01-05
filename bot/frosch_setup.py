# Built-ins
from argparse import ArgumentParser
import asyncio
import asyncpg
import coc
import datetime
from discord import Embed
import logging
import logging.handlers
import traceback
from pathlib import Path

# local
import keys
from frosch_bot import FroschBot

# Global Variables
FROSCH_LOG = Path('logs/frosch.log')
DESCRIPTION = "Bot used to maintain a Clash of Clans database and provide logging"


class BotArgs(ArgumentParser):
    def __init__(self):
        super().__init__(description=DESCRIPTION)
        self.group = self.add_mutually_exclusive_group(required=True)
        self.group.add_argument('--live', help='Run bot in PantherLily shell',
                                action='store_true', dest='live_mode')

        self.group.add_argument('--dev', help='Run bot in devShell shell',
                                action='store_true', dest='dev_mode')

    def parse_the_args(self):
        return self.parse_args()


def setup_logging():
    log = logging.getLogger('root')
    log.setLevel(logging.DEBUG)
    log_handler = logging.handlers.RotatingFileHandler(
        FROSCH_LOG,
        encoding='utf-8',
        maxBytes=100000000,
        backupCount=2
    )

    formatter = logging.Formatter('''\
[%(asctime)s]:[%(levelname)s]:[%(name)s]:[Line:%(lineno)d][Func:%(funcName)s]
[Path:%(pathname)s]
MSG: %(message)s
''', "%d %b %H:%M:%S")
    log_handler.setFormatter(formatter)
    log.addHandler(log_handler)
    log.info('Logger initialized')
    return log


def main(bot_mode, coc):
    log = setup_logging()
    loop = asyncio.get_event_loop()

    try:
        pool = loop.run_until_complete(asyncpg.create_pool(keys.postgres, command_timeout=60))
        bot = FroschBot(bot_config=keys.bot_config(bot_mode), keys=keys,
                        bot_mode=bot_mode, coc=coc, pool=pool)
        bot.run()

    except Exception as error:
        exc = ''.join(traceback.format_exception(type(error), error, error.__traceback__, chain=True))
        print(exc)
        log.error(exc)


if __name__ == '__main__':
    coc_client = coc.login(keys.coc_api['email'], keys.coc_api['password'],
                           throttle_limit=30, key_count=3)
    args = BotArgs().parse_the_args()
    if args.live_mode:
        main('live_mode', coc_client)
    else:
        main('dev_mode', coc_client)
