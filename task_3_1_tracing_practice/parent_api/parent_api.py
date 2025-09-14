from typing import Optional

import httpx
from fastapi import FastAPI
import requests

from common_api.server import run_server
from settings import parent_app_settings


class ParentApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._async_client = httpx.AsyncClient()

        @self.on_event("shutdown")
        async def shutdown_event():
            # Clean up the async client
            await self._async_client.aclose()

        @self.get("/")
        async def root() -> str:
            return "Parent API: root page"

        @self.get("/hello")
        async def hello() -> str:
            r = requests.get(parent_app_settings.child_api_url + "/world")
            return f"Parent API: hello,\n{r.text}"


if __name__ == "__main__":
    parent_app = ParentApp()
    run_server(parent_app, service_name="parent_api", port=10000, log_level="debug")
