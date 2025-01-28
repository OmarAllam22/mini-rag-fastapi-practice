# adding the parent directory to the sys path to enble relative import
import os, sys
parent_dir_path = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(parent_dir_path) if parent_dir_path not in sys.path else None

from helpers.validate_and_load_dotenv_vars import AppConfig

class BaseController:
    def __init__(self):
        self.app_settings = AppConfig()
        self.base_project_dir = parent_dir_path
        

