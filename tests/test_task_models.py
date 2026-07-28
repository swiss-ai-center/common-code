from uuid import uuid4

import pytest
from pydantic import ValidationError

from common_code.tasks.models import ServiceTask


def task_payload():
    return {
        "storage_url": "https://engine.example/storage",
        "task": {
            "id": str(uuid4()),
            "data_in": ["input.json"],
            "status": "pending",
            "service_id": str(uuid4()),
        },
        "callback_url": "https://engine.example/tasks/task-id",
    }


def test_service_task_uses_core_engine_storage_url():
    task = ServiceTask.model_validate(task_payload())

    assert task.storage_url == "https://engine.example/storage"
    assert not any(
        field.startswith("s3_") for field in ServiceTask.model_fields
    )


def test_service_task_rejects_legacy_payload_without_storage_url():
    payload = task_payload()
    payload.pop("storage_url")
    payload.update({
        "s3_access_key_id": "access-key",
        "s3_secret_access_key": "secret-key",
        "s3_region": "region",
        "s3_host": "https://storage.example",
        "s3_bucket": "bucket",
    })

    with pytest.raises(ValidationError):
        ServiceTask.model_validate(payload)
