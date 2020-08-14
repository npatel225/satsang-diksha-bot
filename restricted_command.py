import logging
from functools import wraps

LIST_OF_ADMINS = {263366770, 89505043, 10721297, 180519325}


def restricted_command(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            logging.critical("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)

    return wrapped
