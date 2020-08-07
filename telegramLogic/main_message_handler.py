import telegram
from telegram import Update, Message
from telegram.ext import CallbackContext

from sheetLogic.sheet_messages import SheetMessages


def main_message_handler(update: Update, context: CallbackContext):
    message: Message = update.message
    message.delete()
    message_dict = SheetMessages().message_dict()

    message.reply_text(text=message_dict.get(message.text, "Please run `/start` again"),
                       parse_mode=telegram.ParseMode.MARKDOWN_V2)
