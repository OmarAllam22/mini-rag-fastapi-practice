from enum import Enum
import os

class Constants(Enum):
    LandingDirectory = os.path.dirname(os.path.dirname(__file__)) # used in main.py to expose the main project directory.

    InvalidMimeType = "Iinvalid MIME types:{}, Allowed types are: {}" # used in helpers.validate_and_load_dotenv_vars.py

    InvalidFileTypeResponse = "This file type {} is not supported. Here are the supported file types {}" # used in controllers.data_controller.py
    InvalidFileSizeResponse = "uploaded file of {} bytes larger than the maximum allowed size: {} Mega bytes" # used in controllers.data_controller.py
    SuccessUploadResponse = "File named {} is uploaded correctly" # used in controllers.data_controller.py

    InternalError =  "Your request wasn't executed because there is an internal error. Call the company for more details"

    EmptyDocumentResponse = "Your Document {} has no text. Or cannot be processed. Try another request options (ex: chunk overlap shouldn't be greater than chunk size)" 
    