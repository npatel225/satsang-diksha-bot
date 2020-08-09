from functools import lru_cache

import gspread
from security import Security
from sheetLogic.sheet_config import SheetConfig

class SheetCore(SheetConfig):
    def __init__(self):
        super().__init__()
        self.spreadsheet = self.login.open_by_key(self.sheet_id)

    @property
    @lru_cache(maxsize=None)
    def login(self):
        security = Security()
        security.decrypt_cred()
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
        return gspread.service_account('./credentials.json', scopes=scopes)

    def get_sheet(self, title: str):
        return self.spreadsheet.worksheet(title=title)
