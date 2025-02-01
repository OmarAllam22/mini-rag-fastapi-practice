import os, aiofiles, re
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

    async def write_uploaded_file_and_return_signal(self, file: UploadFile, project_id: int) -> tuple[None|str, str]:
        project_path = self.get_project_path(project_id)
        file_path = os.path.join(project_path, file.filename)
        self.app_settings.logger.info(f"this is a path:{file_path}")
        idx = 1
        try:
            while os.path.exists(file_path):
                matched_idx_list = re.findall(r'(_\d+)(?=\.\w+$)', file_path)
                idx = matched_idx_list[0][-1] if matched_idx_list else idx
                file_path_with_idx_truncated = re.sub(r'(_\d+)(?=\.\w+$)', '', file_path)
                base_path, extension = os.path.splitext(file_path_with_idx_truncated)
                file_path = f"{base_path}_{idx}{extension}"
        except Exception as e:
            self.app_settings.logger.error(e, base_path, file_path_with_idx_truncated)
            return Constants.InternalError.value, file_path
        
        try:
            async with aiofiles.open(file_path,'wb') as f:
                while chunk := await file.read(int(self.app_settings.FILE_MAX_CHUNK_SIZE * 1024 * 1024)):
                    await f.write(chunk)
            return None, file_path
        except Exception as e:
            self.app_settings.logger.error(f"Error while writing file {file.filename} as {e}")
            return Constants.InternalError.value, file_path

