from enum import Enum, auto
from typing import Optional


class CType(Enum):
    INT = auto()
    STRING = auto()
    FLOAT = auto()
    DOUBLE = auto()
    CHAR = auto()
    BOOL = auto()

    INT_ARRAY = auto()
    STRING_ARRAY = auto()
    DOUBLE_ARRAY = auto()
    FLOAT_ARRAY = auto()
    CHAR_ARRAY = auto()
    BOOL_ARRAY = auto()

    VOID = auto()
    NONE = auto()

    @staticmethod
    def get_type(from_string: str, is_function: bool = False) -> Optional['CType']:
        type_map = {
            "int": CType.INT,
            "string": CType.STRING,
            "float": CType.FLOAT,
            "double": CType.DOUBLE,
            "char": CType.CHAR,
            "bool": CType.BOOL,
            "int[]": CType.INT_ARRAY,
            "string[]": CType.STRING_ARRAY,
            "float[]": CType.FLOAT_ARRAY,
            "double[]": CType.DOUBLE_ARRAY,
            "char[]": CType.CHAR_ARRAY,
            "bool[]": CType.BOOL_ARRAY,
            "void": CType.VOID if is_function else CType.NONE
        }
        return type_map.get(from_string, CType.NONE)
