from fastapi import FastAPI

# Note: .env must be loaded before importing the base_router in which variables will be used
from helpers.validate_and_load_dotenv_vars import AppConfig
AppConfig()

from routes.base import base_router
from routes.data import data_router

# Intializing the fastapi app object
app = FastAPI()

# Including the `base router` which is fastapi.APIRouter object
app.include_router(base_router)
app.include_router(data_router)
