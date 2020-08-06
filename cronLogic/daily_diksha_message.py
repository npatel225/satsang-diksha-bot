import os
from datetime import date
from telegram import Bot
from sheetLogic.cron_logic import CronLogic
from sheetLogic.tier_logic import TierLogic

def daily_diksha_message():
    token = os.getenv('TELEGRAM_TOKEN')
    bot: Bot = Bot(token)
    tier_logic = TierLogic()
    data = tier_logic.get_today_data()

    cron_logic = CronLogic()
    users = cron_logic.users()

    for tier, messages in data.items():
        for user_id in users[tier]:
            [bot.send_message(user_id, f'{date.today()}\n\n{message}') for message in messages]

if __name__ == '__main__':
    daily_diksha_message()
