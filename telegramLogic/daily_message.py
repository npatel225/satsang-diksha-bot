import logging
from datetime import datetime, date
from os import getenv
from time import sleep
from typing import List, Tuple, Dict

from telegram.error import Unauthorized
from telegram.ext import CallbackContext, run_async

from sheetLogic.challenge_logic import ChallengeLogic
from sheetLogic.cron_logic import CronLogic


@run_async
def parse_message(context: CallbackContext, chat_id: str, messages: List[Tuple[str, str, str, str]]):
    try:
        for i, message in enumerate(messages):
            logging.info(f'Sending a Message: {chat_id}\n{message}')
            if message[0]:
                context.bot.send_document(chat_id, message[0],
                                          caption=f'{date.today().strftime("%m/%d/%Y")} - {message[3]}', timeout=60)
            elif message[3]:
                context.bot.send_message(chat_id, f'{date.today().strftime("%m/%d/%Y")} - {message[3]}', timeout=60)
            if message[1]:
                context.bot.send_document(chat_id, message[1], timeout=60)
            if message[2]:
                context.bot.send_document(chat_id, message[2], timeout=60)
            if i != 0 and i % 5 == 0:
                sleep(30)
            else:
                sleep(2)
    except Unauthorized:
        logging.warning(f'USER ID has Blocked the Bot. Delete them: {chat_id}')


def daily_message(context: CallbackContext):
    logging.info(f'Entering Daily Message Function: {datetime.now()}')
    tier_logic = ChallengeLogic()
    hour_delta = 0 if getenv('ENV') not in ['DEV', 'LOCAL'] else 24
    data: Dict[str, List[Tuple[str, str, str, str]]] = tier_logic.get_today_data(hour_delta=hour_delta)

    cron_logic = CronLogic()
    users = cron_logic.users()
    logging.info(f'{users}\n {data}')
    for challenge, messages in data.items():
        logging.info(f'Starting Challenge: {challenge}')
        for i, user_id in enumerate(users[challenge]):
            logging.info(f'User ID: {user_id}. Iteration: {i}. Total Iterations: {len(users[challenge])}')
            if i % 25 == 0:
                sleep(5)
            parse_message(context, user_id, messages)
        logging.info(f'Finished Challenge: {challenge}.')
    logging.info(f'Daily Message Done Sending {datetime.now()}')
