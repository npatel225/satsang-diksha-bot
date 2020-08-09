from threading import Thread
from typing import List

from telegram import Update, User, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from send_typing_action import send_typing_action
from sheetLogic.sheet_messages import SheetMessages
from sheetLogic.user_sheet import UserSheet


@send_typing_action
def submit_tier(update: Update, context: CallbackContext):
    query: CallbackQuery = update.callback_query

    tier: str = query.data
    context.user_data.update({'tier': tier})
    phone_number = context.user_data.get('phone_number', '')

    person: User = update.effective_user
    person_id = person.id
    message_dict = SheetMessages().message_dict()

    user_sheet = UserSheet()

    context.bot.delete_message(chat_id=person_id, message_id=query.message.message_id)

    if not user_sheet.uid_check(person_id):
        user_sheet.append_sheet([f'{person_id}', tier, phone_number])
        text = f'{message_dict.get(tier, "Error in getting challenge")}'
        if tier == 'Mahant':
            Thread(target=lambda: context.bot.send_message(chat_id=person_id,
                                                           text='https://baps.box.com/s/oddym4elw4ukv6uv7c8npkyo38bmw826')).start()
        elif tier == 'Pramukh':
            Thread(target=lambda: context.bot.send_message(chat_id=person_id,
                                                           text='https://baps.box.com/s/n7jzempv7ps4y5rbskzq5b6g45hmfd7a')).start()
        elif tier == 'Yogi':
            Thread(target=lambda: context.bot.send_message(chat_id=person_id,
                                                           text='https://baps.box.com/s/0pd4k7gcrbui7qlow861uiojpxxc1qkr')).start()
        elif tier == 'Shastriji':
            Thread(target=lambda: context.bot.send_message(chat_id=person_id,
                                                           text='https://baps.box.com/s/r5hupned1xzbtbf3dx3hbs8lltvt48vw')).start()
    else:
        tier = user_sheet.get_tier(person_id)
        text = f'Your User ID, {person_id}, already exists'

    custom_keyboard: List[List[KeyboardButton]] = list(
        map(lambda m: [KeyboardButton(text=f'{m} - {tier}')], message_dict.get('info')))
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, selective=True)
    Thread(target=lambda: context.bot.send_message(chat_id=person_id, text=text, reply_markup=reply_markup)).start()
    return ConversationHandler.END
