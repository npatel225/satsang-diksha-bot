from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from send_typing_action import send_typing_action


@send_typing_action
def share_number(update: Update, context: CallbackContext):
    contact_keyboard = KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    update.message.reply_text('Please share your contact information with us (required)',
                              reply_markup=reply_markup)
    return '/choose_tier'
