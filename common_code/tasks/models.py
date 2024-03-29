from typing import List, Optional
from pydantic.main import BaseModel
from .enums import TaskStatus
from ..common.enums import FieldDescriptionType
from uuid import UUID


class TaskBase(BaseModel):
    """
    Task model
    """
    data_in: Optional[List[str]] = None
    data_out: Optional[List[str]] = None
    status: Optional[TaskStatus] = None
    service_id: UUID
    pipeline_id: Optional[UUID] = None


class TaskRead(TaskBase):
    """
    Task read model
    """
    id: UUID


class TaskUpdate(BaseModel):
    """
    Task update model
    This model is used to update a task
    """
    service: Optional[str] = None
    url: Optional[str] = None
    data_out: Optional[List[str]] = None
    status: Optional[TaskStatus] = None


class ServiceTaskTask(BaseModel):
    """
    Task update model
    This model is used to update a task
    """
    id: UUID
    data_in: List[str]
    data_out: Optional[List[str]] = None
    status: TaskStatus
    service_id: UUID
    pipeline_execution_id: Optional[UUID] = None


class ServiceTaskBase(BaseModel):
    """
    Base class for Service task
    This model is used in subclasses
    """
    s3_access_key_id: str
    s3_secret_access_key: str
    s3_region: str
    s3_host: str
    s3_bucket: str
    task: ServiceTaskTask
    callback_url: str


class ServiceTask(ServiceTaskBase):
    """
    Service task
    This model is sent from the engine with the information
    """
    pass


class TaskData(BaseModel):
    """
    Task data model used to send data to the service and retrieve data from the service
    """
    data: bytes
    type: FieldDescriptionType
