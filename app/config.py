from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    BACKEND_TYPE: str = "local"
    LOCAL_STORAGE_ROOT_PATH: str = "/data"
    S3_BUCKET_NAME: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_ENDPOINT_URL: Optional[str] = None 

settings = Settings()