from dataclasses import dataclass
from functools import cached_property
from typing import Type, List, Optional, Any

from .. import InspectionError

TYPE_ANY = "typing.Any"
TYPE_UNION = "typing.Union"
TYPE_NONE = str(type(None))
ATTR_ARGS = "__args__"
ATTR_ORIGIN = "__origin__"


@dataclass(init=False)
class AnnotationDetails:
    annotation: Type
    child_details: List["AnnotationDetails"]
    parent_details: Optional["AnnotationDetails"]
    is_nullable: bool = False

    def __init__(self, annotation: Any, parent_details: Optional["AnnotationDetails"] = None) -> None:
        """Initializes the AnnotationDetails object for the annotation provided

        :param annotation: the Python annotation/typing to populate details for
        :param parent_details: (Optional, Default None) the parent annotation details, if any
        """
        self.parent_details = parent_details
        self.child_details = []

        if not hasattr(annotation, ATTR_ORIGIN):
            self.annotation = annotation
            if annotation is None:
                self.is_nullable = True
        else:
            self.annotation = annotation.__origin__
            if not hasattr(annotation, ATTR_ARGS):
                raise InspectionError("Insufficient data on annotation!")

            for arg in annotation.__args__:
                if str(arg) == TYPE_NONE:
                    self.is_nullable = True
                else:
                    self.child_details.append(AnnotationDetails(arg, self))

    @cached_property
    def is_child(self) -> bool:
        """Whether this is a child annotation or not

        :return: True if has parent annotation details, False otherwise
        """
        return self.parent_details is None

    @cached_property
    def is_nested(self) -> bool:
        """Whether this is a nested annotation (ex.: a Union)

        :return: True if nested, False otherwise
        """
        return len(self.child_details) > 0

    @cached_property
    def is_optional(self) -> bool:
        """Whether this is a nullable/optional field

        :return: True if optional, False otherwise
        """
        return self.is_nullable

    @cached_property
    def str_annotation(self) -> str:
        """The string representation of the annotation

        :return: The string representation of the annotation
        """
        return str(self.annotation)

    def value_is_valid_type(self, value: Any) -> bool:
        """Whether the value provided is a valid type for this annotation

        :param value: The value to test
        :return: True if valid, False otherwise
        """
        annotation = AnnotationDetails(type(value))
        return self.is_valid_annotation(annotation)

    def is_valid_annotation(self, annotation: "AnnotationDetails") -> bool:
        """Whether the annotation provided is valid within this annotation

        :param annotation: The annotation to test
        :return: True if valid, False otherwise
        """
        if annotation == self or (annotation.str_annotation == TYPE_NONE and self.is_nullable):
            return True

        for child in self.child_details:
            if child.is_valid_annotation(annotation):
                return True

        return False
