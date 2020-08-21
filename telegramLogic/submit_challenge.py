import logging
from datetime import datetime
from typing import List

from pytz import timezone
from telegram import Update, User, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from restricted_command import unregistered_uid_check
from run_async_func import run_async_func
from send_typing_action import send_typing_action
from sheetLogic.sheet_messages import SheetMessages
from sheetLogic.user_sheet import UserSheet


@send_typing_action
@unregistered_uid_check
def submit_challenge(update: Update, context: CallbackContext, edit=False):
    query: CallbackQuery = update.callback_query

    challenge: str = query.data
    context.user_data.update({'challenge': challenge})

    person: User = update.effective_user
    person_id = person.id
    message_dict = SheetMessages().message_dict()

    user_sheet = UserSheet()

    run_async_func(context.bot.delete_message, chat_id=person_id, message_id=query.message.message_id)
    if edit:
        row, col = user_sheet.get_challenge_cell_from_uid(person_id)
        user_sheet.update_cell(row, col, challenge)
        text = f'{message_dict.get(challenge, "Error in getting challenge")}' \
               f'\n\nNote: You will have to catch up if you have switched to a challenge with more shlokas.'
        logging.info(f'User: {person_id}, successfully changed tiers')
    else:
        user_sheet.append_sheet(
            [f'{person_id}', challenge, datetime.now(tz=timezone('US/Eastern')).date().strftime('%m/%d/%Y')])
        text = f'{message_dict.get(challenge, "Error in getting challenge")}'

        booket_link = f'📚 PDF Booklet - {challenge}'
        run_async_func(context.bot.send_document, chat_id=person_id, document=message_dict.get(booket_link))
        milestone_link = f'📅 Milestones - {challenge}'
        run_async_func(context.bot.send_photo, chat_id=person_id, photo=message_dict.get(milestone_link))

    custom_keyboard: List[List[KeyboardButton]] = list(
        map(lambda m: [KeyboardButton(text=f'{m} - {challenge}')], message_dict.get('info')))
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, selective=True)
    run_async_func(context.bot.send_message, chat_id=person_id, text=text, reply_markup=reply_markup)
    return ConversationHandler.END
