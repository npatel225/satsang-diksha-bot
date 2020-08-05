import logging
import os
import sys
from threading import Thread

from telegram import Update
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.ext import Dispatcher, Updater, Handler, CallbackContext, ConversationHandler, CommandHandler, \
    MessageHandler, Filters, CallbackQueryHandler

from telegramLogic.announcement import announcement
from telegramLogic.broadcast_announcement import broadcast_announcement
from telegramLogic.choose_tier import choose_tier
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
            '/choose_tier': [MessageHandler(Filters.contact, choose_tier)],
            '/tier': [CallbackQueryHandler(submit_tier)]
        },
        fallbacks=[CommandHandler('start', share_number)]
    )
    telegram.add_handler(start_handler)

    announcement_handler = ConversationHandler(
        entry_points=[CommandHandler('announcement', announcement)],
        states={'/announcement': [MessageHandler(Filters.text, broadcast_announcement)]},
        fallbacks=[CommandHandler('announcement', announcement)],
    )
    telegram.add_handler(announcement_handler)

    telegram.dispatcher.add_error_handler(telegram.error_callback)

    telegram.execute()


if __name__ == '__main__':
    main()
