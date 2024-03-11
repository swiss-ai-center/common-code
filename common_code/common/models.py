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


class TestResult(TypedDict):
    """
    Test result model
    name: test name
    result: test result (True/False)
    """

    name: str
    result: bool


class TestResultList(TypedDict):
    """
    Test result list model
    tests_results: list of test results
    tests_passed: True if all tests passed, False otherwise
    """

    results: List[TestResult]
    tests_passed: bool
