from telegram import Update, User
from telegram.ext import CallbackContext, ConversationHandler

from send_typing_action import send_typing_action


@send_typing_action
def submit_tier(update: Update, context: CallbackContext):
    query = update.callback_query

    tier = query.data
    context.user_data.update({'tier': tier})
    phone_number = context.user_data.get('phone_number', '')

    person: User = update.effective_user

    info = f'Phone Number: {phone_number}, Tier: {tier}, User ID: {person.id}'

    query.edit_message_text(text=info)

    return ConversationHandler.END
