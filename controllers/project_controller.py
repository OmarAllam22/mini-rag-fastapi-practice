import os, aiofiles
from enums.constants import Constants
from fastapi import UploadFile
from controllers.base_controller import BaseController

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id : int) -> str:
        project_path = os.path.join(self.app_settings.LANDING_DIRECTORY,"folders",f"project_{project_id}")
        if not os.path.exists(project_path):
            os.mkdir(project_path)
        return project_path

    async def write_uploaded_file_and_return_signal(self, file: UploadFile, project_id: int) -> None | str:
        project_path = self.get_project_path(project_id)
        file_path = os.path.join(project_path, file.filename)
        idx = 1
        while os.path.exists(file_path):
            base_path, extension = os.path.splitext(file_path)
            file_path = f"{base_path}_{idx}{extension}"
        try:
            async with aiofiles.open(file_path,'wb') as f:
                while chunk := await file.read(int(self.app_settings.FILE_MAX_CHUNK_SIZE * 1024 * 1024)):
                    await f.write(chunk)
        except Exception as e:
            self.app_settings.logger.error(f"Error while writing file {file.filename} as {e}")
            return Constants.InternalError.value

