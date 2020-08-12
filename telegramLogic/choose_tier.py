from telegram import Update, Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from send_typing_action import send_typing_action
from sheetLogic.sheet_messages import SheetMessages


@send_typing_action
def choose_challenge(update: Update, context: CallbackContext):
    message_dict = SheetMessages().message_dict()
    message: Message = update.message
    message.delete()
    message.reply_text(message_dict.get('startup_message', 'Jai Swaminarayan'))

    tiers = ('Mahant', 'Pramukh', 'Yogi', 'Shastriji')
    keyboard = [[InlineKeyboardButton(tier, callback_data=f'{tier}')] for tier in tiers]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text("Please select your challenge", reply_markup=reply_markup)

    return '/tier'
