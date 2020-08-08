from collections import defaultdict
from datetime import datetime, date
from typing import Dict, List, Tuple
from gspread import Worksheet

from enums.MessageEnum import MessageEnum
from sheetLogic.sheet_core import SheetCore


class TierLogic(SheetCore):
    def __init__(self):
        super().__init__()
        self.challenge_sheets: Dict[str, Worksheet] = self.get_sheets()

    def get_sheets(self):
        return {tier: self.get_sheet(tier) for tier in self.tiers}

    def get_today_data(self):
        today_data: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        for challenge, tier_sheet in self.challenge_sheets.items():
            for data in tier_sheet.get_all_values()[1:]:
                try:
                    if datetime.strptime(data[MessageEnum.DATE.value], '%m/%d/%Y').date() == date.today():
                        today_data[challenge].append(
                            (data[MessageEnum.AUDIO_LINK.value],
                             f'{data[MessageEnum.GUJARATI_MESSAGE.value]}\n\n{data[MessageEnum.ENGLISH_MESSAGE.value]}',
                             )
                        )
                except ValueError:
                    pass
        return today_data
