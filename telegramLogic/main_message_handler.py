import logging

import telegram
from telegram import Update, Message
from telegram.ext import CallbackContext
import re

from sheetLogic.sheet_messages import SheetMessages


def main_message_handler(update: Update, context: CallbackContext):
    message: Message = update.message
    message.delete()
    message_dict = SheetMessages().message_dict()
    logging.info(f'Button Clicked. User wants {message.text}')

    message.reply_text(text=message_dict
                       .get(message.text, "You have entered an incorrect command. "
                                          "Please enter a valid command. "
                                          "If your buttons are not working, please run `/start` again")
                       )
