import httpx
import pytest

from common_code.common.exceptions import StorageTransferException
from common_code.storage.service import StorageService


class LoggerStub:
    def __init__(self):
        self.errors = []

    def set_source(self, source):
        self.source = source

    def error(self, message):
        self.errors.append(message)


@pytest.mark.asyncio
async def test_get_file_downloads_from_core_engine_and_encodes_key():
    async def handler(request: httpx.Request):
        assert request.method == "GET"
        assert request.url.raw_path == b"/storage/folder%2Finput%20file.json"
        return httpx.Response(200, content=b'{"value": 42}')

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        storage = StorageService(LoggerStub(), http_client)

        result = await storage.get_file(
            "folder/input file.json",
            "https://engine.example/storage/",
        )

    assert result == b'{"value": 42}'


@pytest.mark.asyncio
async def test_get_file_raises_storage_exception_on_http_error():
    async def handler(request: httpx.Request):
        return httpx.Response(404)

    logger = LoggerStub()
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        storage = StorageService(logger, http_client)

        with pytest.raises(
                StorageTransferException,
                match="cannot be downloaded",
        ):
            await storage.get_file("missing.json", "https://engine.example/storage")

    assert logger.errors


@pytest.mark.asyncio
async def test_upload_sends_multipart_file_and_returns_key():
    async def handler(request: httpx.Request):
        body = await request.aread()
        assert request.method == "POST"
        assert request.url.path == "/storage"
        assert b'name="file"' in body
        assert b'filename="result.json"' in body
        assert b"Content-Type: application/json" in body
        assert b'{"value": 42}' in body
        return httpx.Response(200, json={"key": "output-key.json"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        storage = StorageService(LoggerStub(), http_client)

        key = await storage.upload(
            b'{"value": 42}',
            ".json",
            "application/json",
            "https://engine.example/storage/",
        )

    assert key == "output-key.json"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(500),
        httpx.Response(200, content=b"not-json"),
        httpx.Response(200, json={}),
        httpx.Response(200, json={"key": ""}),
    ],
)
async def test_upload_rejects_invalid_responses(response):
    async def handler(request: httpx.Request):
        return response

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        storage = StorageService(LoggerStub(), http_client)

        with pytest.raises(StorageTransferException):
            await storage.upload(
                b"result",
                ".txt",
                "text/plain",
                "https://engine.example/storage",
            )
