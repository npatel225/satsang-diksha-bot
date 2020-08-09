import logging
import os
import sys
from functools import partial
from threading import Thread

from telegram import Update
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.ext import Dispatcher, Updater, Handler, CallbackContext, ConversationHandler, CommandHandler, \
    MessageHandler, Filters, CallbackQueryHandler

from SC import SERVICE_ACCOUNT
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


class Telegram:
    token: str = None
    updater: Updater = None
    dispatcher: Dispatcher = None

    def set_token(self, token: str):
        self.token = token

    def initialize(self):
        if not self.token:
            self.token = os.environ.get('TELEGRAM_TOKEN')

        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def add_handler(self, handler: Handler):
        self.dispatcher.add_handler(handler)

    def stop_and_restart(self):
        """Gracefully stop the Updater and replace the current process with a new one"""
        self.updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(self):
        # update.message.reply_text('Bot is restarting...')
        Thread(target=self.stop_and_restart).start()

    def error_callback(self, update: Update, context: CallbackContext):
        try:
            raise context.error
        except Unauthorized:
            # remove update.message.chat_id from conversation list
            return ConversationHandler.END
        except BadRequest:
            # handle malformed requests - read more below!
            return ConversationHandler.END
        except TimedOut:
            # handle slow connection problems
            return ConversationHandler.END
        except NetworkError:
            # handle other connection problems
            return ConversationHandler.END
        except ChatMigrated:
            # the chat_id of a group has changed, use e.new_chat_id instead
            return ConversationHandler.END
        except TelegramError as err:
            # handle all other telegram related errors
            logging.error(err)
            self.restart()
            context.bot.send_message(263366770, f'Error reached, restarting bot. {err}')
            return ConversationHandler.END

    def execute(self):
        PORT = int(os.environ.get("PORT", "8443"))
        APP_NAME = os.environ.get("APP_NAME")
        self.updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=self.token)
        self.updater.bot.set_webhook(f"{APP_NAME}{self.token}")
        self.updater.idle()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    telegram = Telegram()
    telegram.initialize()
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
