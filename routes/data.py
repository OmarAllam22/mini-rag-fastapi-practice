from fastapi import APIRouter, UploadFile
import os, sys
from controllers.data_controller import DataController

app_name = os.getenv("APP_NAME")
app_version = os.getenv("APP_VERSION")

data_router = APIRouter(
    prefix=f"/{app_name}/{app_version}",
    tags = ['data', 'upload-files']
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: int, file: UploadFile):
    return  DataController().is_valid_uploaded_file(file)