from typing import List, Optional, Any
from pydantic import BaseModel
from .enums import FieldDescriptionType, ExecutionUnitTagName, ExecutionUnitTagAcronym


class FieldDescription(BaseModel):
    """
    Field description model
    """
    name: str
    type: List[FieldDescriptionType]
    format_hint: Optional[Any] = None


class ExecutionUnitTag(BaseModel):
    """
    Service tag model
    """
    name: ExecutionUnitTagName
    acronym: ExecutionUnitTagAcronym
