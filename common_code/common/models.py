from typing import List
from pydantic import BaseModel
from .enums import FieldDescriptionType, ExecutionUnitTagName, ExecutionUnitTagAcronym


class FieldDescription(BaseModel):
    """
    Field description model
    """
    name: str
    type: List[FieldDescriptionType]


class ExecutionUnitTag(BaseModel):
    """
    Service tag model
    """
    name: ExecutionUnitTagName
    acronym: ExecutionUnitTagAcronym
