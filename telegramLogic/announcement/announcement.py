from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from restricted_command import restricted_command


@restricted_command
def announcement(update: Update, context: CallbackContext):
    tiers = ['Mahant', 'Pramukh', 'Yogi', 'Shastriji', 'All']
    keyboard = [[InlineKeyboardButton(tier, callback_data=f'{tier}')] for tier in tiers]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please select your challenge", reply_markup=reply_markup)

    return '/challenge'
