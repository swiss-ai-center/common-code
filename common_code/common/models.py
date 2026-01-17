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


class TestResult(TypedDict):
    """
    Test result model
    This model is used to return a test result
    name: test name
    result: test result (True/False)
    """

    name: str
    result: bool


class TestResultList(TypedDict):
    """
    Test result list model
    This model is used to return a list of test results used in the service test
    tests_results: list of test results
    tests_passed: True if all tests passed, False otherwise
    """

    results: List[TestResult]
    tests_passed: bool
