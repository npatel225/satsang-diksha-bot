import logging

from telegram.error import Unauthorized
from telegram.ext import run_async


@run_async
def run_async_func(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Unauthorized:
        logging.error(f'USER ID has Blocked the Bot. Delete them: {kwargs.get("uid", "None")}')
