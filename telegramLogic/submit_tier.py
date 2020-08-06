from telegram import Update, User, CallbackQuery
from telegram.ext import CallbackContext, ConversationHandler

from send_typing_action import send_typing_action
from sheetLogic.sheet_messages import SheetMessages
from sheetLogic.user_sheet import UserSheet


@send_typing_action
def submit_tier(update: Update, context: CallbackContext):
    query: CallbackQuery = update.callback_query

    tier = query.data
    context.user_data.update({'tier': tier})
    phone_number = context.user_data.get('phone_number', '')

    person: User = update.effective_user
    person_id = person.id

    user_sheet = UserSheet()

    if not user_sheet.uid_check(person_id):
        user_sheet.append_sheet([f'{person_id}', tier, phone_number])
        message_dict = SheetMessages().message_dict()
        query.edit_message_text(text=f'{message_dict.get(tier, "Error in getting challenge")}', )
    else:
        query.edit_message_text(text=f'Your User ID, {person_id}, already exists')

    return ConversationHandler.END
