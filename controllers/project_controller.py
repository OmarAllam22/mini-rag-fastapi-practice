import os

from controllers.base_controller import BaseController

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id : int) -> str:
        project_path = os.path.join(self.app_settings.LANDING_DIRECTORY,"folders",f"project_{project_id}")
        if not os.path.exists(project_path):
            os.mkdir(project_path)
        return project_path
