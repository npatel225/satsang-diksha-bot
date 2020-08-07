import ast

from sheetLogic.sheet_core import SheetCore


class SheetMessages(SheetCore):
    def __init__(self):
        super().__init__()

    def get_sheet(self):
        return super().get_sheet("Messages")

    def message_dict(self):
        return {title: self.__custom_eval(message) for title, message, *_ in self.get_sheet().get_all_values()}

    @staticmethod
    def __custom_eval(message):
        try:
            return ast.literal_eval(message)
        except ValueError:
            return message
        except SyntaxError:
            return message
