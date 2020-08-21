import logging
from datetime import datetime, time
from functools import partial
from os import getenv

from telegram.ext import ConversationHandler, CommandHandler, \
    MessageHandler, Filters, CallbackQueryHandler, JobQueue

from SC import SERVICE_ACCOUNT
from telegramLogic.announcement.announcement import announcement
from telegramLogic.announcement.broadcast_choose_challenge import broadcast_choose_challenge
from telegramLogic.announcement.broadcast_entity import broadcast_entity
from telegramLogic.choose_tier import choose_challenge
from telegramLogic.daily_message import daily_message
from telegramLogic.main_message_handler import main_message_handler
from telegramLogic.submit_challenge import submit_challenge
from telegramLogic.today_message import today_message
from telegram_class import Telegram


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    telegram = Telegram()
    telegram.initialize()

    job_queue: JobQueue = telegram.job_queue
    logging.info(f'Time Right now: {datetime.now()}')
    if getenv('ENV') == 'LOCAL':
        job_queue.run_once(daily_message, 0)
    else:
        job_queue.run_daily(daily_message,
                            time=time(hour=int(getenv('HOUR', '5')), minute=int(getenv('MINUTE', '30'))))

    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', choose_challenge)],
        states={
            '/tier': [CallbackQueryHandler(submit_challenge)]
        },
        fallbacks=[CommandHandler('start', choose_challenge)]
    )
    telegram.add_handler(start_handler)
    announcement_handler = ConversationHandler(
        entry_points=[CommandHandler('announcement', announcement)],
        states={
            '/challenge': [
                CommandHandler('cancel', lambda update, context: ConversationHandler.END),
                CallbackQueryHandler(broadcast_choose_challenge),
            ],
            '/announcement': [
                CommandHandler('cancel', lambda update, context: ConversationHandler.END),
                MessageHandler(Filters.text | Filters.photo | Filters.document | Filters.video, broadcast_entity),
            ]
        },
        fallbacks=[CommandHandler('announcement', announcement)],
    )
    telegram.add_handler(announcement_handler)

    edit_handler = ConversationHandler(
        entry_points=[CommandHandler(['change', 'edit'], choose_challenge)],
        states={
            '/tier': [CallbackQueryHandler(partial(submit_challenge, edit=True))],
        },
        fallbacks=[CommandHandler(['change', 'edit'], choose_challenge)],
    )
    telegram.add_handler(edit_handler)

    today_handler = CommandHandler(['today'], today_message)
    telegram.add_handler(today_handler)

    message_handler = MessageHandler(Filters.text, main_message_handler)
    telegram.add_handler(message_handler)

    telegram.dispatcher.add_error_handler(telegram.error_callback)
    telegram.execute()


if __name__ == '__main__':
    main()
