from controllers.base_controller import BaseController
from controllers.project_controller import ProjectController
from enums.constants import Constants
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self, project_id: int):
        super().__init__()
        self.project_id = project_id

    async def check_file_validity(self, file: UploadFile) -> dict:
        """
        # Alternative code to get th type content:
        import mimetypes
        mimetypes.types_map # outputs dict['content_type','file_extension']
        mimetypes.guess_type('file_path') # outputs the content_type of the file   
        #or 
        print(mimetypes.types_map['.txt']) -> 'text/plain'
        """

        if (file.content_type not in self.app_settings.ALLOWED_MIME_TYPES):
            signal = Constants.InvalidFileTypeResponse.value.format(file.content_type, self.app_settings.ALLOWED_MIME_TYPES)
            self.app_settings.logger.info(signal)
            return {
                    "valid": False,
                    "signal" : signal
                }
            # raise ValueError(f"this file type {file.content_type} is not supported. Here are the supported file types {self.app_settings.ALLOWED_MIME_TYPES}")
            # if we typed this raise, we got error from the code ... and in request, error in code is seen as internal server error
        
        elif (file.size  > self.app_settings.MAX_FILE_SIZE * 1024 * 1024):
            signal = Constants.InvalidFileSizeResponse.value.format(file.size, self.app_settings.MAX_FILE_SIZE)
            self.app_settings.logger.info(signal)
            return {
                    "valid": False,
                    "signal" : signal
                }            
        else:
            write_signal = await ProjectController().write_uploaded_file_and_return_signal(file ,self.project_id) # write the uploaded file in the folders directory
            signal = Constants.SuccessUploadResponse.value.format(file.filename) if not write_signal else write_signal
            self.app_settings.logger.info(signal) if not write_signal else None  # as write_signal is already logged in project_controller.py as error when there was an exception. 
            return {
                    "valid": True,
                    "signal" : signal
                }
            