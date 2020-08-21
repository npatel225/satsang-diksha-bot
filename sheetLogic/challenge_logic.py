from collections import defaultdict
from datetime import datetime, date, timedelta
from functools import partial
from typing import Dict, List, Tuple
from gspread import Worksheet

from enums.MessageEnum import MessageEnum
from sheetLogic.sheet_core import SheetCore


class ChallengeLogic(SheetCore):
    def __init__(self):
        super().__init__()
        self.challenge_sheets: Dict[str, Worksheet] = self.get_sheets()

    def get_sheets(self):
        return {tier: self.get_sheet(tier) for tier in self.tiers}

    @staticmethod
    def __challenge_message_parse(data, hour_delta, today_data, challenge):
        try:
            given_datetime = datetime.strptime(data[MessageEnum.DATE.value], '%m/%d/%Y') - timedelta(
                hours=hour_delta)
            if given_datetime.date() == date.today():
                today_data[challenge].append(
                    (data[MessageEnum.VIDEO_LINK.value],
                     data[MessageEnum.GRAPHIC_LINK.value],
                     data[MessageEnum.MOTIVATIONAL_LINK.value],
                     data[MessageEnum.MESSAGE.value],
                     )
                )
        except ValueError:
            pass

    def get_today_data(self, hour_delta=0) -> Dict[str, List[Tuple[str, str, str, str]]]:
        today_data: Dict[str, List[Tuple[str, str, str, str]]] = defaultdict(list)
        for challenge, tier_sheet in self.challenge_sheets.items():
            parser = partial(self.__challenge_message_parse, hour_delta=hour_delta, today_data=today_data,
                             challenge=challenge)
            list(map(parser, tier_sheet.get_all_values()[1:]))

        return today_data
