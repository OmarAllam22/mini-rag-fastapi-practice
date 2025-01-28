import os, sys
parent_dir_path = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(parent_dir_path) if parent_dir_path not in sys.path else None

from controllers.base_controller import BaseController
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def is_valid_uploaded_file(self, file: UploadFile) -> bool | str :
        """
        # Alternative code to get th type content:
        import mimetypes
        mimetypes.types_map # outputs dict['content_type','file_extension']
        mimetypes.guess_type('file_path') # outputs the content_type of the file   
        #or 
        print(mimetypes.types_map['.txt']) -> 'text/plain'
        """

        if (file.content_type not in self.app_settings.ALLOWED_MIME_TYPES):
            return f"this file type {file.content_type} is not supported. Here are the supported file types {self.app_settings.ALLOWED_MIME_TYPES}"
            # raise ValueError(f"this file type {file.content_type} is not supported. Here are the supported file types {self.app_settings.ALLOWED_MIME_TYPES}")
            # if we typed this raise, we got error from the code ... and in request, error in code is seen as internal server error
        
        elif (file.size  > self.app_settings.MAX_FILE_SIZE * 1024 * 1024):
            return f"uploaded file of {file.size} bytes larger than the maximum allowed size: {self.app_settings.MAX_FILE_SIZE} Mega bytes"
            # return ValueError(f"uploaded file of {file.size} bytes larger than the maximum allowed size: {self.app_settings.MAX_FILE_SIZE} Mega bytes")
        else:
            return True