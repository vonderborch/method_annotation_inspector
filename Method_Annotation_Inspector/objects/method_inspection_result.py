from dataclasses import dataclass


@dataclass(init=False)
class MethodInspectionResult:
    method_name: str
    method_type: int
    return_type_details: int
    parameters: Dict[str, ...]

    def __init__(self) -> None:
        ...
