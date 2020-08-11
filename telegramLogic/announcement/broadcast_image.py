import logging
from time import sleep

from telegram import Update, Message
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, ConversationHandler, run_async, JobQueue

from restricted_command import restricted_command
from sheetLogic.user_sheet import UserSheet


@run_async
def single_broadcast(context, uid, photo, message):
    try:
        logging.info(f'Sending Announcement to {uid}')
        context.bot.send_photo(uid, photo.file_id, caption=message.caption)
    except Unauthorized:
        logging.error(f'USER ID has Blocked the Bot. Delete them: {uid}')


@restricted_command
def broadcast_image(update: Update, context: CallbackContext):
    job_queue: JobQueue = context.job_queue

    def cb(c: CallbackContext):
        message: Message = update.message
        user_sheet = UserSheet()
        challenge = c.job.context.get('broadcast_challenge', 'All')
        if challenge == 'All':
            challenge = None

        for i, uid in enumerate(user_sheet.get_challenge_uids(challenge=challenge)):
            sleep(i % 9)
            if photos := message.photo:
                single_broadcast(c, uid, photos[-1], message)
            logging.info(f'Iteration Completed {i}')

    job_queue.run_once(cb, 10, context=context.user_data)

    return ConversationHandler.END
