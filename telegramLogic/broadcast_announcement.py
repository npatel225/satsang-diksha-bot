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
    challenge = context.user_data.get('broadcast_challenge', 'All')
    if challenge == 'All':
        challenge = None
    for uid in user_sheet.get_challenge_uids(challenge=challenge):
        thread = Thread(target=lambda: context.bot.send_message(chat_id=uid, text=message.text, ))
        thread.start()
        threads.append(thread)

    list((thread.join() for thread in threads))
    return ConversationHandler.END
