from typing import Optional

from fastapi import FastAPI

from server import run_server


class ChildApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @self.get("/")
        async def root() -> str:
            return "Child API: root page"

        @self.get("/world")
        async def hello() -> str:
            return str(2 / 0)
            return f"Child API: world!"


if __name__ == "__main__":
    child_app = ChildApp()
    run_server(child_app, service_name="child_api", port=10001, log_level="debug")
