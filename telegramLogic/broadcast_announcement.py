import telegram
from telegram import Update, Message
from telegram.ext import CallbackContext, ConversationHandler

from threading import Thread

from restricted_command import restricted_command
from sheetLogic.user_sheet import UserSheet


@restricted_command
def broadcast_announcement(update: Update, context: CallbackContext):
    message: Message = update.message
    user_sheet = UserSheet()
    threads = []
    for uid in user_sheet.get_all_uid():
        thread = Thread(target=lambda: context.bot.send_message(chat_id=uid, text=message.text,
                                                                parse_mode=telegram.ParseMode.MARKDOWN_V2))
        thread.start()
        threads.append(thread)

    list((thread.join() for thread in threads))
    return ConversationHandler.END
