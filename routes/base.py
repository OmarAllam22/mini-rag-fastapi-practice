from fastapi import APIRouter
import os
app_name = os.getenv("APP_NAME")
app_version = os.getenv("APP_VERSION")

base_router = APIRouter(
    prefix=f"/{app_name}/{app_version}",
    tags= [f"{app_name}_{app_version}"]
)

@base_router.get("/")
def welcome():
    return {
        "message" : "Hello World",
        "app_name" : app_name,
        "app_version" : app_version
    }