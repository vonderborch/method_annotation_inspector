from dataclasses import dataclass
from inspect import signature, Parameter, Signature, ismethod, isfunction, isclass
from typing import Callable, Dict

from . import AnnotationDetails, ParameterDetails
from ..enums import MethodType
from .. import InspectionError


@dataclass(init=False)
class MethodInspectionResult:
    method_name: str
    method_type: MethodType
    return_annotation_details: AnnotationDetails
    parameters: Dict[str, ParameterDetails]
    _inspection_details: Signature

    def __init__(self, function: Callable) -> None:
        self._inspection_details = signature(function)
        self.method_name = function.__name__

        # determine the type of the method
        if ismethod(function):
            if isclass(function.__self__):
                self.method_type = MethodType.CLASS_CLASS_METHOD
            else:
                self.method_type = MethodType.CLASS_INSTANCE_METHOD
        elif isfunction(function):
            if self.method_name != function.__qualname__:
                self.method_type = MethodType.CLASS_STATIC_METHOD
            else:
                self.method_type = MethodType.FUNCTION
        else:
            raise InspectionError("Unknown function type!")

        if self._inspection_details.return_annotation == Parameter.empty:
            raise InspectionError("Method must be fully type-annotated!")

        # get annotation details on the return for the method
        self.return_annotation_details = AnnotationDetails(self._inspection_details.return_annotation, None)

        # inspect the parameters
        self.parameters = {}
        i: int
        name: str
        details: Parameter
        for i, (name, details) in enumerate(self._inspection_details.parameters.items()):
            special_parameter = False
            raise_if_missing_annotation = True

            if i == 0 and self.method_type in [MethodType.CLASS_CLASS_METHOD, MethodType.CLASS_INSTANCE_METHOD]:
                special_parameter = True
                raise_if_missing_annotation = False

            self.parameters[name] = ParameterDetails(
                name=name,
                argument_position=i,
                details=details,
                special_parameter=special_parameter,
                raise_if_missing_annotation=raise_if_missing_annotation,
            )
