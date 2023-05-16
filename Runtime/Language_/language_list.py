from typing import Any


class LanguageList:
    def __init__(self):
        self.values = []

    def append(self, value: Any):
        self.values.append(value)

    def get_ele_at(self, index: int) -> Any:
        return self.values[index] if 0 <= index < len(self.values) else None

    def length(self) -> int:
        return len(self.values)

    def set_at_index(self, index: int, value: Any) -> bool:
        if index == self.length():
            self.values.insert(index, value)
        elif 0 <= index < self.length():
            self.values[index] = value
        else:
            return False
        return True
