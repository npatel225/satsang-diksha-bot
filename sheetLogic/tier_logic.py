from collections import defaultdict
from datetime import datetime, date
from typing import Dict, List, Tuple

from gspread import Worksheet

from sheetLogic.sheet_core import SheetCore

DATE = 0
GUJARATI_MESSAGE = 1
ENGLISH_MESSAGE = 2
AUDIO_LINK = 3


class TierLogic(SheetCore):
    def __init__(self):
        super().__init__()
        self.tier_sheets: Dict[str, Worksheet] = self.get_sheets()

    def get_sheets(self):
        return {tier: self.get_sheet(tier) for tier in self.tiers}

    def get_today_data(self):
        today_data: Dict[str, List[str]] = defaultdict(list)
        for tier, tier_sheet in self.tier_sheets.items():
            for data in tier_sheet.get_all_values()[1:]:
                if datetime.strptime(data[DATE], '%m/%d/%Y').date() == date.today():
                    today_data[data].append(f'{data[GUJARATI_MESSAGE]}\n\n{data[ENGLISH_MESSAGE]}\n\n{data[AUDIO_LINK]}')
        return today_data
