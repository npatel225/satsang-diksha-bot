import logging
from time import sleep

from telegram import Update, Message
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, ConversationHandler, run_async

from restricted_command import restricted_command
from sheetLogic.user_sheet import UserSheet


@run_async
def single_broadcast(context, uid, video, message):
    try:
        logging.info(f'Sending Announcement to {uid}')
        context.bot.send_video(uid, video.file_id, caption=message.caption)
    except Unauthorized:
        logging.error(f'USER ID has Blocked the Bot. Delete them: {uid}')


@restricted_command
def broadcast_video(update: Update, context: CallbackContext):
    message: Message = update.message
    user_sheet = UserSheet()
    challenge = context.user_data.get('broadcast_challenge', 'All')
    if challenge == 'All':
        challenge = None

    for i, uid in enumerate(user_sheet.get_challenge_uids(challenge=challenge)):
        sleep(i % 10)
        if video := message.video:
            single_broadcast(context, uid, video, message)
        logging.info(f'Iteration Completed {i}')

    return ConversationHandler.END
