from telegram import Update, Message
from telegram.ext import CallbackContext

from restricted_command import restricted_command


@restricted_command
def announcement(update: Update, context: CallbackContext):
    message: Message = update.message
    message.reply_text("Please reply with your announcement. Note: Once sent, it cannot be edited")
    return message.text
