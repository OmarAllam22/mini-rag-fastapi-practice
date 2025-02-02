# adding the parent directory to the sys path to enble relative import

from helpers.validate_and_load_dotenv_vars import AppConfig

class BaseController:
    def __init__(self):
        self.app_settings = AppConfig() # contains all the .env variables in addition to get_settings() method
        