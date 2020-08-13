import logging
from time import sleep

from telegram import Update, Message
from telegram.ext import CallbackContext, ConversationHandler, JobQueue

from restricted_command import restricted_command
from run_async_func import run_async_func
from sheetLogic.user_sheet import UserSheet


@restricted_command
def broadcast_entity(update: Update, context: CallbackContext):
    job_queue: JobQueue = context.job_queue

    def cb(c: CallbackContext):
        message: Message = update.message
        user_sheet = UserSheet()
        challenge = c.job.context.get('broadcast_challenge', 'All')
        if challenge == 'All':
            challenge = None

        for i, uid in enumerate(user_sheet.get_challenge_uids(challenge=challenge)):
            sleep(max(2, i % 6))
            logging.info(f'Sending Announcement to {uid}')
            if photos := message.photo:
                run_async_func(c.bot.send_photo, chat_id=uid, photo=photos[-1], caption=message.caption)
            elif video := message.video:
                run_async_func(c.bot.send_video, chat_id=uid, video=video, caption=message.caption)
            elif document := message.document:
                run_async_func(c.bot.send_document, chat_id=uid, document=document.file_id, caption=message.caption)
            else:
                run_async_func(c.bot.send_message, chat_id=uid, text=message.text)
            logging.info(f'Iteration Completed {i}')
        logging.info(f'Announcement has finished sending')

    job_queue.run_once(cb, 0, context=context.user_data)

    return ConversationHandler.END
