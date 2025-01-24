from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field , FilePath
from dotenv import load_dotenv
import os

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

    def __init__(self, **data):
        # this is to load the environment variables in the python session.
        super().__init__(**data)  # must call the super class here & must pass the **data (which are the class defined variables) as the same in case of using @dataclass
        load_dotenv(self.dotenv_file)



