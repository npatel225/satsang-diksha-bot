import functools
import json
import os
from datetime import timedelta, datetime
from functools import lru_cache

import gspread
from oauth2client.client import AccessTokenCredentials
from oauth2client.service_account import ServiceAccountCredentials

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


token_file = "./access_token.txt"  # token file including the authorization data
now = int(datetime.now().timestamp())


class SheetCore(SheetConfig):
    def __init__(self):
        super().__init__()
        self.spreadsheet = self.login.open_by_key(self.sheet_id)

    @property
    def login(self):
        security = Security()
        security.decrypt_cred()
        credentials = self.getCredential()
        return gspread.authorize(credentials)

    def getNewAccessToken(self, credential_file):
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scope)
        gc = gspread.authorize(credentials)
        token_response = gc.auth.token_response
        token_response['limitTime'] = token_response['expires_in'] + now - 300
        with open(token_file, mode='w') as f:
            json.dump(token_response, f)
        return token_response['access_token']

    def getCredential(self):
        if os.path.exists(token_file):
            with open(token_file) as f:
                token = json.load(f)
            access_token = token['access_token'] if token['limitTime'] > now else self.getNewAccessToken(
                './credentials.json')
        else:
            access_token = self.getNewAccessToken('./credentials.json')
        return AccessTokenCredentials(access_token, None)

    def get_sheet(self, title: str):
        return self.spreadsheet.worksheet(title=title)
