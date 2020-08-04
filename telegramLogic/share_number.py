import threading

from telegram import Update, Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from send_typing_action import send_typing_action


@send_typing_action
def share_number(update: Update, context: CallbackContext):
    query: CallbackQuery = update.callback_query
    message: Message = query.message
    region = query.data

    context.user_data.update({'region': region})

    contact_keyboard = KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)

    t1 = threading.Thread(target=lambda: context.bot.delete_message(message.chat_id, message.message_id))
    t1.start()

    t2 = threading.Thread(target=lambda: message.reply_text('Please share your contact information with us (required)',
                                                            reply_markup=reply_markup))
    t2.start()
    t1.join()
    t2.join()

    return '/choose_tier'
