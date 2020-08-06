from telegram import Update, Message, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from send_typing_action import send_typing_action


@send_typing_action
def choose_challenge(update: Update, context: CallbackContext):
    message: Message = update.message
    contact = message.contact
    context.user_data.update({'phone_number': contact.phone_number})

    tiers = ['Mahant', 'Pramukh', 'Yogi', 'Shastriji', ]

    keyboard = [[InlineKeyboardButton(tier, callback_data=f'{tier}')] for tier in tiers]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please select your challenge", reply_markup=reply_markup)

    return '/tier'
