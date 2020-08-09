import logging
import os
from datetime import date
from threading import Thread
from typing import List, Dict, Tuple

from telegram import Bot

from sheetLogic.cron_logic import CronLogic
from sheetLogic.tier_logic import TierLogic


def daily_diksha_message():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    token = os.getenv('TELEGRAM_TOKEN')
    bot: Bot = Bot(token)
    tier_logic = TierLogic()
    data: Dict[str, List[Tuple[str, str, str]]] = tier_logic.get_today_data()

    cron_logic = CronLogic()
    users = cron_logic.users()
    threads = []
    logging.debug(data)
    for challenge, messages in data.items():
        for user_id in users[challenge]:
            for message in messages:
                logging.debug(message)
                if message[0]:
                    thread = Thread(
                        target=lambda: bot.send_document(user_id, message[0], caption=f'{date.today()}'))
                    thread.start()
                    threads.append(thread)
                if message[1]:
                    thread = Thread(
                        target=lambda: bot.send_document(user_id, message[1]))
                    thread.start()
                    threads.append(thread)
                if message[2]:
                    thread = Thread(
                        target=lambda: bot.send_message(user_id, message[2])
                    )
                    thread.start()
                    threads.append(thread)
    [thread.join() for thread in threads]


if __name__ == '__main__':
    daily_diksha_message()
