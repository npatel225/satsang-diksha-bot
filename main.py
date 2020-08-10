import logging
from functools import partial
from datetime import datetime, date, time
from time import sleep
from typing import Dict, List, Tuple


from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, \
    MessageHandler, Filters, CallbackQueryHandler, JobQueue, run_async

from SC import SERVICE_ACCOUNT
from sheetLogic.cron_logic import CronLogic
from sheetLogic.tier_logic import TierLogic
from telegramLogic.announcement.announcement import announcement
from telegramLogic.announcement.broadcast_announcement import broadcast_announcement
from telegramLogic.announcement.broadcast_choose_challenge import broadcast_choose_challenge
from telegramLogic.announcement.broadcast_document import broadcast_document
from telegramLogic.announcement.broadcast_image import broadcast_image
from telegramLogic.announcement.broadcast_video import broadcast_video
from telegramLogic.choose_tier import choose_challenge
from telegramLogic.main_message_handler import main_message_handler
from telegramLogic.share_number import share_number
from telegramLogic.submit_tier import submit_tier
from telegram_class import Telegram


@run_async
def parse_message(context: CallbackContext, user_id: str, messages: List[Tuple[str, str, str, str]]):
    for i, message in enumerate(messages):
        logging.info(f'Sending a Message: {user_id}')
        if message[0]:
            context.bot.send_document(user_id, message[0], caption=f'{date.today()}')
        if message[1]:
            context.bot.send_document(user_id, message[1])
        if message[2]:
            context.bot.send_document(user_id, message[2])
        if message[3]:
            context.bot.send_message(user_id, message[3])
        sleep(i * 60)


def daily_message(context: CallbackContext):
    logging.info(f'Entering Daily Message Function: {datetime.now()}')
    tier_logic = TierLogic()
    hour_delta = 0
    data: Dict[str, List[Tuple[str, str, str, str]]] = tier_logic.get_today_data(hour_delta=hour_delta)

    cron_logic = CronLogic()
    users = cron_logic.users()
    logging.info(f'{users}\n {data}')
    for challenge, messages in data.items():
        for i, user_id in enumerate(users[challenge]):
            if i != 0 and i % 20 == 0:
                logging.info('Sleeping Peacefully')
                sleep(180)
            parse_message(context, user_id, messages)


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    telegram = Telegram()
    telegram.initialize()

    job_queue: JobQueue = telegram.job_queue
    logging.info(f'Time Right now: {datetime.now()}')
    job_queue.run_daily(daily_message, time=time(hour=14, minute=25))

    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', share_number)],
        states={
            '/choose_tier': [MessageHandler(Filters.contact, choose_challenge)],
            '/tier': [CallbackQueryHandler(submit_tier)]
        },
        fallbacks=[CommandHandler('start', share_number)]
    )
    telegram.add_handler(start_handler)
    announcement_handler = ConversationHandler(
        entry_points=[CommandHandler('announcement', announcement)],
        states={
            '/challenge': [CallbackQueryHandler(broadcast_choose_challenge)],
            '/announcement': [
                MessageHandler(Filters.text, broadcast_announcement),
                MessageHandler(Filters.document, broadcast_document),
                MessageHandler(Filters.photo, broadcast_image),
                MessageHandler(Filters.video, broadcast_video),
            ]
        },
        fallbacks=[CommandHandler('announcement', announcement)],
    )
    telegram.add_handler(announcement_handler)

    edit_handler = ConversationHandler(
        entry_points=[CommandHandler('edit', share_number)],
        states={
            '/choose_tier': [MessageHandler(Filters.contact, choose_challenge)],
            '/tier': [CallbackQueryHandler(partial(submit_tier, edit=True))],
        },
        fallbacks=[CommandHandler('edit', share_number)],
    )

    telegram.add_handler(edit_handler)

    message_handler = MessageHandler(Filters.text, main_message_handler)

    telegram.add_handler(message_handler)

    telegram.dispatcher.add_error_handler(telegram.error_callback)
    telegram.execute()


if __name__ == '__main__':
    main()
