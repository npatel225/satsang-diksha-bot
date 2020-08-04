from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from send_typing_action import send_typing_action


@send_typing_action
def submit_tier(update: Update, context: CallbackContext):
    query = update.callback_query

    tier = query.data
    context.user_data.update({'tier': tier})
    phone_number = context.user_data.get('phone_number', '')

    info = f'Phone Number: {phone_number}, Tier: {tier}'

    query.edit_message_text(text=info)

    return ConversationHandler.END
