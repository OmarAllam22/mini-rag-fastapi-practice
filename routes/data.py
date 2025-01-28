from fastapi import APIRouter, UploadFile
import os, sys
from controllers.data_controller import DataController
parent_dir_path = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(parent_dir_path) if parent_dir_path not in sys.path else None

app_name = os.getenv("APP_NAME")
app_version = os.getenv("APP_VERSION")

data_router = APIRouter(
    prefix=f"/{app_name}/{app_version}",
    tags = ['data', 'upload-files']
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: int, file: UploadFile):
    return {"is_valid": DataController().is_valid_uploaded_file(file),
            "app_name": app_name,
            "app_version": app_version,
            "project_id": project_id}