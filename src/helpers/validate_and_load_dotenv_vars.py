from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field , FilePath, field_validator
from dotenv import load_dotenv
import os, mimetypes

# to strict the one whoe defines the .env to set valid MIME types
VALID_MIME_TYPES = mimetypes.types_map

class AppConfig(BaseSettings):
    
    dotenv_file : FilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)),".env") 
    
    # model_config is a reserved name that must be overwritten
    model_config = SettingsConfigDict(
        env_file = dotenv_file,
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
                raise ValueError(f"Iinvalid MIME types:{value}, Allowed types are: {VALID_MIME_TYPES}")
        return dotenv_mimi_values
    
    MAX_FILE_SIZE: int = Field(default=10, description="value here is in MegaBytes")

    # this is to load the environment variables in the python session.
    def __init__(self, **data):
        super().__init__(**data)  # must call the super class here & must pass the **data (which are the class defined variables) as the same in case of using @dataclass
        load_dotenv(self.dotenv_file)

    # redundant method as it returns the instance itself.
    def get_settings(self):
        return self


