from os import getenv

from telegram import Update
from telegram.ext import CallbackContext

from restricted_command import unregistered_uid_check
from sheetLogic.challenge_logic import ChallengeLogic
from sheetLogic.user_sheet import UserSheet
from telegramLogic.daily_message import parse_message


@unregistered_uid_check
def today_message(update: Update, context: CallbackContext):
    chat_id = update.effective_user.id

    user_sheet = UserSheet()
    challenge_logic = ChallengeLogic()

    challenge_cell = user_sheet.get_challenge_cell_from_uid(chat_id)
    challenge = user_sheet.sheet.cell(*challenge_cell).value

    hour_delta = 0 if getenv('ENV') not in ['DEV', 'LOCAL'] else 24
    messages = challenge_logic.get_today_data(hour_delta=hour_delta)[challenge]

    parse_message(context, chat_id, messages)
