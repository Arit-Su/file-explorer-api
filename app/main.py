from fastapi import FastAPI, Depends, HTTPException
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator

from .config import settings
from .storage.base import StorageBackend, Item
from .storage.local import LocalStorageBackend
from .storage.s3 import S3StorageBackend

app = FastAPI(
    title="File Explorer API",
    description="An API to browse files from various storage backends.",
    version="1.0.0"
)

# Exposes a /metrics endpoint for Prometheus
Instrumentator().instrument(app).expose(app)

def get_storage_backend() -> StorageBackend:
    """Dependency that provides the configured storage backend."""
    backend_type = settings.BACKEND_TYPE.lower()
    
    if backend_type == 'local':
        return LocalStorageBackend(root_path=settings.LOCAL_STORAGE_ROOT_PATH)
    
    if backend_type == 's3':
        if not all([settings.S3_BUCKET_NAME, settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY]):
            raise ValueError("S3 backend requires S3_BUCKET_NAME, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY")
        return S3StorageBackend(
            bucket_name=settings.S3_BUCKET_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL
        )
        
    raise ValueError(f"Unsupported backend type: {backend_type}")

@app.get("/", response_model=List[Item], summary="List root directory")
async def list_root(storage: StorageBackend = Depends(get_storage_backend)):
    try:
        return storage.list("")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{path:path}", response_model=List[Item], summary="List items in a path")
async def list_path(path: str, storage: StorageBackend = Depends(get_storage_backend)):
    try:
        return storage.list(path)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))