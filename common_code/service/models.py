from abc import ABCMeta, abstractmethod
from typing import List, Optional
from pydantic import BaseModel
from ..common.models import FieldDescription
from ..common.models import ExecutionUnitTag
from .enums import ServiceStatus


class Service(BaseModel, metaclass=ABCMeta):
    """
    Service model
    """

    name: str
    slug: str
    url: str
    summary: str
    description: Optional[str] = None
    status: ServiceStatus
    data_in_fields: Optional[List[FieldDescription]] = None
    data_out_fields: Optional[List[FieldDescription]] = None
    tags: Optional[List[ExecutionUnitTag]] = None
    docs_url: Optional[str] = None
    has_ai: Optional[bool] = None

    def get_data_in_fields(self):
        """
        Data in fields
        """
        return self.data_in_fields

    def get_data_out_fields(self):
        """
        Data out fields
        """
        return self.data_out_fields

    def get_tags(self):
        """
        Tags
        """
        return self.tags

    @abstractmethod
    def process(self, data):
        pass

    @abstractmethod
    def main_test(self, data):
        pass
