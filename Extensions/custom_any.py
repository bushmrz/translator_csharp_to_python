# custom_any.py
from typing import Any, List

class CustomAny:
    def __init__(self, value: Any):
        self.value = value

    def can_be_casted_to_same_type(self, other: Any) -> bool:
        def get_type(value: Any) -> str:
            if isinstance(value, int):
                return "Int"
            elif isinstance(value, float):
                return "Double"
            elif isinstance(value, str):
                return "String"
            elif isinstance(value, list):
                if value and isinstance(value[0], (int, float, str)):
                    return f"[{get_type(value[0])}]"
            return None

        type1 = get_type(self)
        type2 = get_type(other)
        print(type1,type2)
        return type1 == type2

    def __eq__(self, other):
        if not isinstance(other, CustomAny):
            return False
        return (self.value is None and other.value is None) or (self.value is not None and self.can_be_casted_to_same_type(other) and self.value == other.value)
