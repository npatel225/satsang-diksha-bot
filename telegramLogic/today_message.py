from telegram import Update
from telegram.ext import CallbackContext

from sheetLogic.challenge_logic import ChallengeLogic
from sheetLogic.user_sheet import UserSheet
from telegramLogic.daily_message import parse_message


def today_message(update: Update, context: CallbackContext):
    chat_id = update.effective_user.id

    user_sheet = UserSheet()

    if not user_sheet.uid_check(chat_id):
        update.message.reply_text('We could not locate you. Please run `/start` to register', quote=True)
        return

    challenge_cell = user_sheet.get_challenge_cell_from_uid(chat_id)

    challenge = user_sheet.sheet.cell(*challenge_cell).value

    challenge_logic = ChallengeLogic()

    messages = challenge_logic.get_today_data()[challenge]

    parse_message(context, chat_id, messages)
