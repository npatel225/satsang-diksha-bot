import logging
from functools import wraps

from telegram.ext import ConversationHandler

from sheetLogic.user_sheet import UserSheet

LIST_OF_ADMINS = {263366770, 89505043, 10721297, 180519325}


def restricted_command(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            logging.critical(f"Unauthorized access denied for {user_id}.")
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def unregistered_uid_check(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        chat_id = update.effective_user.id
        user_sheet = UserSheet()
        if chat_id not in user_sheet.uid_check(chat_id):
            update.message.reply_text('We could not locate you. Please run `/start` to register')
            return ConversationHandler.END
        return func(update, context, *args, **kwargs)

    return wrapped


def registered_uid_check(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        chat_id = update.effective_user.id
        user_sheet = UserSheet()
        if chat_id in user_sheet.uid_check(chat_id):
            update.message.reply_text(
                f'Your User ID, {chat_id}, already exists. Please run `/change` to change your challenge')
            return ConversationHandler.END
        return func(update, context, *args, **kwargs)

    return wrapped
