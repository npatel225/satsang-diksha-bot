import logging
from datetime import datetime

import gspread

from security import Security
from sheetLogic.sheet_config import SheetConfig
from SC import SERVICE_ACCOUNT

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
        # credentials = self.getCredential()
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
        global SERVICE_ACCOUNT

        if SERVICE_ACCOUNT:
            logging.info(f"SERVICE_ACCOUNT.auth.expired {SERVICE_ACCOUNT.auth.expired}")
            if SERVICE_ACCOUNT.auth.expired:
                SERVICE_ACCOUNT = gspread.service_account('./credentials.json', scopes=scopes)
                logging.info('Service Account successfully refreshed')
            return SERVICE_ACCOUNT
        else:
            SERVICE_ACCOUNT = gspread.service_account('./credentials.json', scopes=scopes)
            return SERVICE_ACCOUNT

    def get_sheet(self, title: str):
        return self.spreadsheet.worksheet(title=title)
