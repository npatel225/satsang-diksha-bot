from os import getenv
from typing import Tuple

class SheetConfig:
    sheet_id = getenv('GSHEET_ID')
    tiers: Tuple[str, str, str, str] = ('Mahant', 'Pramukh', 'Yogi', 'Shastriji',)
