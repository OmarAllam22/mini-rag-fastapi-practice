from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse
import os
from controllers.data_controller import DataController
from controllers.project_controller import ProjectController

app_name = os.getenv("APP_NAME")
app_version = os.getenv("APP_VERSION")

data_router = APIRouter(
    prefix=f"/{app_name}/{app_version}",
    tags = ['data', 'upload-files']
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: int, file: UploadFile):
    file_validity_dict = await DataController(project_id).check_file_validity(file)
    if file_validity_dict['valid']:
#        none_msg_or_exception = await ProjectController().write_uploaded_file(file ,project_id) # write the uploaded file in the folders directory
        return JSONResponse(
            status_code= status.HTTP_200_OK,
            content= {
                "upload_status": file_validity_dict['signal']
            }
        )
    else:
        JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content= {
                "upload_status": file_validity_dict['signal']
            }
        )