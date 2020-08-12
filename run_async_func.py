from telegram.ext import run_async


@run_async
def run_async_func(func, chat_id, item):
    func(chat_id, item)
