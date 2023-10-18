from dataclasses import dataclass
from typing import Type


@dataclass(init=False)
class ParameterDetails:
    annotation: Type

    def __init__(self) -> None:
        ...
