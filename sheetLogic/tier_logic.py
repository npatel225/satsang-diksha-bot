from collections import defaultdict
from datetime import datetime, date
from typing import Dict, List

from gspread import Worksheet

from enums.messageEnum import messageEnum
from sheetLogic.sheet_core import SheetCore


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
                if datetime.strptime(data[messageEnum.DATE], '%m/%d/%Y').date() == date.today():
                    today_data[tier].append(
                        f'{data[messageEnum.GUJARATI_MESSAGE]}\n\n{data[messageEnum.ENGLISH_MESSAGE]}\n\n{data[messageEnum.AUDIO_LINK]}')
        return today_data
