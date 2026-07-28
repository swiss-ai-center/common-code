from urllib.parse import quote

import httpx
from fastapi import Depends

from ..common.exceptions import StorageTransferException
from ..http_client import HttpClient
from ..logger.logger import Logger, get_logger


class StorageService:
    def __init__(
            self,
            logger: Logger = Depends(get_logger),
            http_client: HttpClient = Depends(),
    ):
        self.logger = logger
        self.http_client = http_client
        self.logger.set_source(__name__)

    async def upload(
            self,
            data: bytes,
            file_extension_with_dot: str,
            content_type: str,
            storage_url: str,
    ) -> str:
        """
        Upload a file through the Core Engine storage endpoint.

        :param data: File contents.
        :param file_extension_with_dot: File extension, including its leading dot.
        :param content_type: MIME type of the file.
        :param storage_url: Core Engine storage endpoint.
        :return: Storage key returned by the Core Engine.
        """
        try:
            response = await self.http_client.post(
                storage_url.rstrip("/"),
                files={
                    "file": (
                        f"result{file_extension_with_dot}",
                        data,
                        content_type,
                    )
                },
                timeout=None,
            )
            response.raise_for_status()
            payload = response.json()
            key = payload.get("key") if isinstance(payload, dict) else None
            if not isinstance(key, str) or not key:
                raise StorageTransferException(
                    "Storage upload response does not contain a valid key"
                )
            return key
        except StorageTransferException:
            raise
        except (httpx.HTTPError, ValueError) as e:
            self.logger.error(f"Error uploading file through Core Engine: {e}")
            raise StorageTransferException(
                "File cannot be uploaded through Core Engine"
            ) from e

    async def get_file(
            self,
            key: str,
            storage_url: str,
    ) -> bytes:
        """
        Get a file through the Core Engine storage endpoint.

        :param key: Key of the file to retrieve.
        :param storage_url: Core Engine storage endpoint.
        :return: File contents.
        """
        try:
            encoded_key = quote(key, safe="")
            response = await self.http_client.get(
                f"{storage_url.rstrip('/')}/{encoded_key}",
                timeout=None,
            )
            response.raise_for_status()
            return response.content
        except httpx.HTTPError as e:
            self.logger.error(f"Error downloading file through Core Engine: {e}")
            raise StorageTransferException(
                "File cannot be downloaded through Core Engine"
            ) from e
