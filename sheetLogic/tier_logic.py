from typing import List

from gspread import Worksheet

from sheetLogic.sheet_core import SheetCore


class TierLogic(SheetCore):
    def __init__(self):
        super().__init__()
        self.tiers = ('Mahant', 'Pramukh', 'Yogi', 'Shastriji')
        self.tier_sheets: List[Worksheet] = self.get_sheets()

    def get_sheets(self):
        return [self.get_sheet(tier) for tier in self.tiers]
