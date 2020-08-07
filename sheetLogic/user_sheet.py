from typing import List

from sheetLogic.sheet_core import SheetCore


class UserSheet(SheetCore):
    def __init__(self):
        super().__init__()
        self.sheet = self.get_sheet()

    def get_sheet(self):
        return super().get_sheet('Users')

    def append_sheet(self, values: List[str]):
        return self.sheet.append_row(values, value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS')

    def get_challenge_uids(self, challenge=None):
        if challenge is None:
            return (person[0] for person in self.sheet.get_all_values()[1:])
        else:
            return (person[0] for person in self.sheet.get_all_values()[1:] if person[1] == challenge)

    def get_tier(self, uid: int):
        for person in self.sheet.get_all_values()[1:]:
            if person[0] == f'{uid}':
                return person[1]

    def uid_check(self, uid: int):
        return f'{uid}' in set(self.get_challenge_uids())
