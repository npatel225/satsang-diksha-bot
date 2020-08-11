from collections import defaultdict
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple
from gspread import Worksheet
from pytz import timezone

from enums.MessageEnum import MessageEnum
from sheetLogic.sheet_core import SheetCore


class TierLogic(SheetCore):
    def __init__(self):
        super().__init__()
        self.challenge_sheets: Dict[str, Worksheet] = self.get_sheets()

    def get_sheets(self):
        return {tier: self.get_sheet(tier) for tier in self.tiers}

    def get_today_data(self, tz='UTC') -> Dict[str, List[Tuple[str, str, str, str]]]:
        today_data: Dict[str, List[Tuple[str, str, str, str]]] = defaultdict(list)
        for challenge, tier_sheet in self.challenge_sheets.items():
            for data in tier_sheet.get_all_values()[1:]:
                try:
                    given_datetime = datetime.strptime(data[MessageEnum.DATE.value], '%m/%d/%Y')
                    if given_datetime.date() == datetime.now(tz=timezone(tz)).date():
                        today_data[challenge].append(
                            (data[MessageEnum.VIDEO_LINK.value],
                             data[MessageEnum.GRAPHIC_LINK.value],
                             data[MessageEnum.MOTIVATIONAL_LINK.value],
                             data[MessageEnum.MESSAGE.value],
                             )
                        )
                except ValueError:
                    pass
        return today_data
