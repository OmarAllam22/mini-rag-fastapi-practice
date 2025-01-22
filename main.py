from fastapi import FastAPI

# Load the variables in .env as global variables
from dotenv import load_dotenv
load_dotenv(".env")

# Note: .env must be loaded before importing the base_router in which variables will be used
from routes.base import base_router

# Intializing the fastapi app object
app = FastAPI()

# Including the `base router` which is fastapi.APIRouter object
app.include_router(base_router)
