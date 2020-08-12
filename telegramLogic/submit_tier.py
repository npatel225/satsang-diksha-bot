import logging
from datetime import datetime
from pytz import timezone
from threading import Thread
from typing import List

from telegram import Update, User, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from send_typing_action import send_typing_action
from sheetLogic.sheet_messages import SheetMessages
from sheetLogic.user_sheet import UserSheet


@send_typing_action
def submit_tier(update: Update, context: CallbackContext, edit=False):
    query: CallbackQuery = update.callback_query

    tier: str = query.data
    context.user_data.update({'tier': tier})

    person: User = update.effective_user
    person_id = person.id
    message_dict = SheetMessages().message_dict()

    user_sheet = UserSheet()

    context.bot.delete_message(chat_id=person_id, message_id=query.message.message_id)
    if edit:
        logging.info(f'Switching tier to: {tier}')
        row, col = user_sheet.get_tier_from_uid(person_id)
        if user_sheet.update_cell(row, col, tier) != -1:
            text = f'{message_dict.get(tier, "Error in getting challenge")}' \
                   f'\n\nNote: You will have to catch up if you have switched to a challenge with more shlokas.'
            logging.info(f'User: {person_id}, successfully changed tiers')
        else:
            text = f'We could not locate you. Please run `/start` to register'
            logging.error(f'User does not exist: {person_id}')
    elif not user_sheet.uid_check(person_id):
        user_sheet.append_sheet(
            [f'{person_id}', tier, datetime.now(tz=timezone('US/Eastern')).date().strftime('%m/%d/%Y')])
        text = f'{message_dict.get(tier, "Error in getting challenge")}'
        if tier == 'Mahant':
            Thread(target=lambda: context.bot.send_photo(
                chat_id=person_id,
                photo='https://baps.box.com/shared/static/y72d037zjyfy9tk1awagtjmd6atr8i35.jpg?v=3'
            )).start()
            Thread(target=lambda: context.bot.send_document(
                chat_id=person_id,
                document='https://baps.box.com/shared/static/7drpp40u7wnu8fvmhuy0o8etw4dpvlbb.pdf?v=3')).start()
        elif tier == 'Pramukh':
            Thread(target=lambda: context.bot.send_photo(
                chat_id=person_id,
                photo='https://baps.box.com/shared/static/zqt5mckhhwbkml7gzqnrd4a52ovojaux.jpg?v=3'
            )).start()
            Thread(target=lambda: context.bot.send_document(
                chat_id=person_id,
                document='https://baps.box.com/shared/static/4lip8e1511riapolm61g76gvof5jw601.pdf?v=3')).start()
        elif tier == 'Yogi':
            Thread(target=lambda: context.bot.send_photo(
                chat_id=person_id,
                photo='https://baps.box.com/shared/static/n6nkf7tqj1z3587o5x4tmsh7awgp0hyi.jpg?v=3'
            )).start()
            Thread(target=lambda: context.bot.send_document(
                chat_id=person_id,
                document='https://baps.box.com/shared/static/y05xpgl4xstubzvzhal111i95wwr6by6.pdf?v=3')).start()
        elif tier == 'Shastriji':
            Thread(target=lambda: context.bot.send_photo(
                chat_id=person_id,
                photo='https://baps.box.com/shared/static/fdqym3f6centtgeqai0km6cwlu4rovbt.jpg?v=3'
            )).start()
            Thread(target=lambda: context.bot.send_document(
                chat_id=person_id,
                document='https://baps.box.com/shared/static/auvtp12v83dc91qun2blgtz0nfcusdxh.pdf?v=3')).start()
    else:
        tier = user_sheet.get_tier(person_id)
        text = f'Your User ID, {person_id}, already exists. Please run `/change` to change your challenge'

    custom_keyboard: List[List[KeyboardButton]] = list(
        map(lambda m: [KeyboardButton(text=f'{m} - {tier}')], message_dict.get('info')))
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, selective=True)
    Thread(target=lambda: context.bot.send_message(chat_id=person_id, text=text, reply_markup=reply_markup)).start()
    return ConversationHandler.END
