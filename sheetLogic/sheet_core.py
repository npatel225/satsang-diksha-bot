import gspread
from security import Security
from sheetLogic.sheet_config import SheetConfig

class SheetCore(SheetConfig):
    def __init__(self):
        super().__init__()
        self.spreadsheet = self.login().open_by_key('1R86uo07qmaUl96fymiNXFsGtJuO3RnlDIXWiGius1cM')

    @staticmethod
    def login():
        security = Security()
        security.decrypt_cred()
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
        return gspread.service_account('./credentials.json', scopes=scopes)

    def get_sheet(self, title: str):
        return self.spreadsheet.worksheet(title=title)
