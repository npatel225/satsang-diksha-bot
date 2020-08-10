from threading import Thread
from time import sleep

from telegram import Update, Message
from telegram.ext import CallbackContext, ConversationHandler, run_async

from restricted_command import restricted_command
from sheetLogic.user_sheet import UserSheet


@run_async
def single_broadcast(context, uid, video, message):
    context.bot.send_video(uid, video.file_id, caption=message.caption)


@restricted_command
def broadcast_video(update: Update, context: CallbackContext):
    message: Message = update.message
    user_sheet = UserSheet()
    challenge = context.user_data.get('broadcast_challenge', 'All')
    if challenge == 'All':
        challenge = None

    for i, uid in enumerate(user_sheet.get_challenge_uids(challenge=challenge)):
        if i != 0 and i % 25 == 0:
            sleep(30)
        if video := message.video:
            single_broadcast(context, uid, video, message)

    return ConversationHandler.END
