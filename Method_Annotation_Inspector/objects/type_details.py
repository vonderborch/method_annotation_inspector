from dataclasses import dataclass
from typing import Type


@dataclass(init=False)
class TypeDetails:
    annotation: Type

    def __init__(self) -> None:
        ...
