from enum import Enum


class ParameterType(Enum):
    SPECIAL_PARAMETER = -1
    POSITIONAL_ONLY = 0
    KEYWORD_ONLY = 3
    VAR_POSITIONAL = 2
    VAR_KEYWORD = 4
    POSITIONAL_OR_KEYWORD = 1
