from os import getenv


class SheetConfig:
    sheet_id = getenv('GSHEET_ID')
    tiers = ('Mahant', 'Pramukh', 'Yogi', 'Shastriji',)
