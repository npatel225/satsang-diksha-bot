from collections import defaultdict
from typing import Dict, List

from sheetLogic.user_sheet import UserSheet


class CronLogic(UserSheet):
    def __init__(self):
        super().__init__()

    def users(self):
        users: Dict[str, List[str]] = defaultdict(list)
        for tier in self.tiers:
            for user in self.sheet.get_all_values()[1:]:
                if user[1] == tier:
                    users[tier].append(user[1])
        return users
