from threading import Thread

from telegram import Update, Message
from telegram.ext import CallbackContext, ConversationHandler

from restricted_command import restricted_command
from sheetLogic.user_sheet import UserSheet


@restricted_command
def broadcast_image(update: Update, context: CallbackContext):
    message: Message = update.message
    user_sheet = UserSheet()
    threads = []
    challenge = context.user_data.get('broadcast_challenge', 'All')
    if challenge == 'All':
        challenge = None

    for uid in user_sheet.get_challenge_uids(challenge=challenge):
        if photos := message.photo:
            for photo in photos:
                thread = Thread(target=lambda: context.bot.send_photo(uid, photo.file_id, caption=message.caption))
                thread.start()
                threads.append(thread)

    list(map(lambda t: t.join(), threads))
    return ConversationHandler.END
