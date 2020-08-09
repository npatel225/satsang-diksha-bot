import functools
from datetime import timedelta, datetime
from functools import lru_cache

import gspread
from security import Security
from sheetLogic.sheet_config import SheetConfig


def cache(seconds: int, maxsize: int = 128, typed: bool = False):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize, typed=typed)(func)
        func.delta = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.delta

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.delta

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


class SheetCore(SheetConfig):
    def __init__(self):
        super().__init__()
        self.spreadsheet = self.login.open_by_key(self.sheet_id)

    @property
    @cache(100)
    def login(self):
        security = Security()
        security.decrypt_cred()
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
        return gspread.service_account('./credentials.json', scopes=scopes)

    def get_sheet(self, title: str):
        return self.spreadsheet.worksheet(title=title)
