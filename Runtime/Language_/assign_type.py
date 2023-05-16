from enum import Enum


class AssignType(Enum):
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    SLASH_ASSIGN = "/="
    STAR_ASSIGN = "*="
    NONE = "none"

    @staticmethod
    def get_type(string):
        for assign_type in AssignType:
            if assign_type.value == string:
                return assign_type
        return None
