from datetime import date

from telegram import Update
from telegram.ext import CallbackContext

from send_typing_action import send_typing_action
from sheetLogic.cron_logic import CronLogic
from sheetLogic.tier_logic import TierLogic


@send_typing_action
def test_cron(update: Update, context: CallbackContext):
    tier_logic = TierLogic()
    cron_logic = CronLogic()

    data = tier_logic.get_today_data()
    users = cron_logic.users()
    print("Test Cron")
    for tier, message in data.items():
        for user_id in users[tier]:
            print("USER", user_id, f'{date.today()}\n\n{message}')
            context.bot.send_message(user_id, f'{date.today()}\n\n{message}')
