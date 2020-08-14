import logging
import os
import sys
from logging import Handler
from threading import Thread

from telegram import Update, TelegramError
from telegram.error import ChatMigrated, NetworkError, BadRequest, TimedOut, Unauthorized
from telegram.ext import Updater, Dispatcher, CallbackContext, ConversationHandler, JobQueue


class Telegram:
    token: str = None
    updater: Updater = None
    job_queue: JobQueue = None
    dispatcher: Dispatcher = None

    def set_token(self, token: str):
        self.token = token

    def initialize(self):
        if not self.token:
            self.token = os.environ.get('TELEGRAM_TOKEN')

        self.updater = Updater(self.token, workers=10, use_context=True,
                               request_kwargs={'read_timeout': 20, 'connect_timeout': 20})
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.dispatcher.job_queue

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
        port = int(os.environ.get("PORT", "8443"))
        app_name = os.environ.get("APP_NAME")
        self.updater.start_webhook(listen='0.0.0.0', port=port, url_path=self.token)
        self.updater.bot.set_webhook(f"{app_name}{self.token}")
        self.updater.idle()
