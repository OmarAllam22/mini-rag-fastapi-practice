from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field , FilePath, field_validator
from dotenv import dotenv_values, load_dotenv
import os, mimetypes, logging
from enums.constants import Constants   # this relative import is handled in main.py after adding this LandingDirectory to sys.path


LANDING_DIRECTORY = Constants.LandingDirectory.value 

# to strict the one whoe defines the .env to set valid MIME types
VALID_MIME_TYPES = mimetypes.types_map

class AppConfig(BaseSettings):
    
    dotenv_path : FilePath = os.path.join(LANDING_DIRECTORY,".env") 

    # this is to load the environment variables in the python session.
    def __init__(self, **data):
        super().__init__(**data)  # must call the super class here & must pass the **data (which are the class defined variables) as the same in case of using @dataclass
        env_dict = dotenv_values(self.dotenv_path)
        env_dict['LANDING_DIRECTORY'] = LANDING_DIRECTORY
        with open(".env", 'w') as env_file:
            for key, value in env_dict.items():
                env_file.write(f"{key} = {value}\n")
        load_dotenv(self.dotenv_path)

        logging.basicConfig(filename=os.path.join('app.log'),
                                    filemode='a', 
                                    format='%(asctime)s - %(levelname)s - %(message)s')
        AppConfig.logger = logging


    # model_config is a reserved name that must be overwritten
    model_config = SettingsConfigDict(
        env_file = dotenv_path,
        case_sensitive=True, # to make the reading from .env case-sensitive to env variables defined below
        extra="forbid"       # not to allow for extra env variables in the .env than those defined below
    )
    
    # the .env vars in which no extra vars allowed  
    APP_NAME: str = Field(max_length=15)
    APP_VERSION : str = Field(max_length=10, default="01.00.00")
    GOOGLE_API_KEY : str = Field(min_length=5)
    
    ALLOWED_MIME_TYPES: list[str] = Field(description="list of allowed MIME types")  
    @field_validator("ALLOWED_MIME_TYPES")
    def validate_mime_types_set(cls, dotenv_mimi_values:list[str]):   # important note here to use the cls not the self (because validation is run before the instance is created so we cannot use self)
        for value in dotenv_mimi_values:
            if value not in VALID_MIME_TYPES.values():
                raise ValueError(Constants.InvalidMimeType.value.format(value, VALID_MIME_TYPES))
        return dotenv_mimi_values
    
    MAX_FILE_SIZE: int = Field(default=10, description="value here is in MegaBytes")
    FILE_MAX_CHUNK_SIZE: float = Field(default=.512, description="value here is in MegaBytes")

    LANDING_DIRECTORY: str = Field(description="Absolute path for the main directory of the project. Is automatically set.")
    @field_validator('LANDING_DIRECTORY')
    def validate_dir_existence(cls, path : str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"This path: {path} in your .env LANDING_DIRECTORY doesn't exist.")
        return path

    # redundant method as it returns the instance itself.
    def get_settings(self):
        return self


