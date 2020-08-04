from datetime import date

from telegram import Update
from telegram.ext import CallbackContext

from send_typing_action import send_typing_action
from sheetLogic.cron_logic import CronLogic
from sheetLogic.tier_logic import TierLogic


@send_typing_action
def test_cron(update: Update, context: CallbackContext):
    tier_logic = TierLogic()
    data = tier_logic.get_today_data()

    cron_logic = CronLogic()
    users = cron_logic.users()

    for tier, messages in data.items():
        for user_id in users[tier]:
            [context.bot.send_message(user_id, f'{date.today()}\n\n{message}') for message in messages]
