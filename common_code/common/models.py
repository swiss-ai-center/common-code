from typing import List
from typing_extensions import TypedDict
from .enums import FieldDescriptionType, ExecutionUnitTagName, ExecutionUnitTagAcronym


class FieldDescription(TypedDict):
    """
    Field description model
    """
    name: str
    type: List[FieldDescriptionType]


class ExecutionUnitTag(TypedDict):
    """
    Service tag model
    """
    name: ExecutionUnitTagName
    acronym: ExecutionUnitTagAcronym
