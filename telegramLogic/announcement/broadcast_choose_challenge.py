from telegram import Update, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def broadcast_choose_challenge(update: Update, context: CallbackContext):
    query: CallbackQuery = update.callback_query
    broadcast_challenge = query.data

    context.user_data.update({'broadcast_challenge': broadcast_challenge})

    query.edit_message_text("Please reply with your announcement. Note: Once sent, it cannot be edited")

    return '/announcement'
