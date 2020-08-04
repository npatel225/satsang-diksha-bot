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

    UserSheet().append_sheet([f'{person.id}', tier, phone_number])

    query.edit_message_text(text=f'You have successfully registered. Your ID is {person.id}')

    return ConversationHandler.END
