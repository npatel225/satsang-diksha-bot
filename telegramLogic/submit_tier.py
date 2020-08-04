from telegram import Update, User
from telegram.ext import CallbackContext, ConversationHandler

from send_typing_action import send_typing_action
from sheetLogic.user_sheet import UserSheet


@send_typing_action
def submit_tier(update: Update, context: CallbackContext):
    query = update.callback_query

    tier = query.data
    context.user_data.update({'tier': tier})
    phone_number = context.user_data.get('phone_number', '')

    person: User = update.effective_user
    person_id = person.id

    user_sheet = UserSheet()

    if not user_sheet.uid_check(person_id):
        user_sheet.append_sheet([f'{person_id}', tier, phone_number])

        query.edit_message_text(text=f'You have successfully registered. Your ID is {person_id}')
    else:
        query.edit_message_text(text=f'An user with the ID, {person_id}, already exists')

    return ConversationHandler.END
