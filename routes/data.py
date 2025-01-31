from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse
import os
from controllers.data_controller import DataController
from helpers.pydantic_schemas_for_validation import FileProcessRequestSchema

app_name = os.getenv("APP_NAME")
app_version = os.getenv("APP_VERSION")

data_router = APIRouter(
    prefix=f"/{app_name}/{app_version}",
    tags = ['data', 'upload-files']
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: int, file: UploadFile):
    file_validity_dict = await DataController(project_id).check_file_validity(file) # using await because it is async function
    if file_validity_dict['valid']:
        return JSONResponse(
            status_code= status.HTTP_200_OK,
            content= {
                "upload_status": file_validity_dict['signal'],
                "written_file_name": file_validity_dict['written_file_name']
            }
        )
    else:
        JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content= {
                "upload_status": file_validity_dict['signal']
            }
        )

@data_router.post("/process/{project_id}")
async def process_file(project_id: int, process_request_schema: FileProcessRequestSchema):
    data_controller_obj = DataController(project_id = project_id)
    content = data_controller_obj.process_single_file(process_request_schema = process_request_schema)
    if content:
        return content
#        return JSONResponse(
#            status_code= status.HTTP_200_OK,
#            content = {"file_content" : content}
#        )
    else:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { "msg": data_controller_obj.file_empty_msg_or_cannot_parsed_msg}
        )
