from enum import Enum


class MethodType(Enum):
    FUNCTION = "function"
    CLASS_STATIC_METHOD = "class_static_method"
    CLASS_CLASS_METHOD = "class_class_method"
    CLASS_INSTANCE_METHOD = "class_instance_method"
