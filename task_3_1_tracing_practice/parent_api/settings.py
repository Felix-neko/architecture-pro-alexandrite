from pydantic_settings import BaseSettings


class ParentAppSettings(BaseSettings):
    child_api_url: str = "http://localhost:10001"


parent_app_settings = ParentAppSettings()
