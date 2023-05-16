from typing import Any, List

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

    return type1 == type2

Any.__eq__ = lambda self, other: (self is None and other is None) or (self is not None and self.can_be_casted_to_same_type(other) and self == other)
