import os
from time import sleep
from datetime import date
from threading import Thread
from typing import List, Dict, Tuple

from telegram import Bot

from sheetLogic.cron_logic import CronLogic
from sheetLogic.tier_logic import TierLogic


def parse_message(bot: Bot, user_id: str, messages: List[Tuple[str, str, str, str]]):
    for i, message in enumerate(messages):
        if message[0]:
            bot.send_document(user_id, message[0], caption=f'{date.today()}')
        if message[1]:
            bot.send_document(user_id, message[1])
        if message[2]:
            bot.send_document(user_id, message[2])
        if message[3]:
            bot.send_message(user_id, message[3])
        sleep(i * .03)


def daily_diksha_message():
    token = os.getenv('TELEGRAM_TOKEN')
    bot: Bot = Bot(token)
    tier_logic = TierLogic()
    data: Dict[str, List[Tuple[str, str, str, str]]] = tier_logic.get_today_data()

    cron_logic = CronLogic()
    users = cron_logic.users()
    threads = []
    for challenge, messages in data.items():
        for user_id in users[challenge]:
            thread = Thread(target=parse_message, args=(bot, user_id, messages,))
            thread.start()
            threads.append(thread)

    [thread.join() for thread in threads]


if __name__ == '__main__':
    daily_diksha_message()
