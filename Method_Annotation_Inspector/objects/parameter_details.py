from dataclasses import dataclass
from functools import cached_property
from inspect import Parameter, _empty
from typing import Any

from .. import InspectionError, NONE_PROVIDED
from ..enums import ParameterType
from ..objects import AnnotationDetails


@dataclass(init=False)
class ParameterDetails:
    name: str
    default: Any
    parameter_type: ParameterType
    argument_position: int
    annotation: AnnotationDetails

    _details: Parameter

    def __init__(self, name: str, argument_position: int, details: Parameter, special_parameter: bool = False, raise_if_missing_annotation: bool = True) -> None:
        """Initializes the parameter details object

        :param name: The name of the parameter
        :param argument_position: The position of the argument in the method
        :param details: Inspection details for the parameter
        :param special_parameter: Whether this is a special parameter (self, cls, etc.) or not
        :param raise_if_missing_annotation: Whether to raise an error if we are missing annotation details or not
        """
        self.name = name

        self.special_parameter = special_parameter
        self.argument_position = argument_position
        self._details = details

        if details.annotation == Parameter.empty and raise_if_missing_annotation:
            raise InspectionError(f"Method must be fully type-annotated, missing annotation for parameter #{argument_position + 1} '{name}'")

        self.default = NONE_PROVIDED if details.default == _empty else details.default

        self.parameter_type = ParameterType(int(details.kind)) if not special_parameter else ParameterType.SPECIAL_PARAMETER

        self.annotation = AnnotationDetails(details.annotation, None)

    @cached_property
    def has_default(self) -> bool:
        """Returns whether this parameter has a default value or not

        :return: True if the parameter has a default, False otherwise
        """
        return self.default != NONE_PROVIDED
