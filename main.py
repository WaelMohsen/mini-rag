import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader

load_dotenv(".env.example")

app = FastAPI()

API_KEY_HEADER = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)

def verify_api_key(api_key: str | None = Depends(api_key_header)):
    expected_api_key = "941305a0-c7ba-4678-b364-2efb7aa234f2"
    if not expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key is not configured.",
        )
    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )

class HelloWorldApi:
    def __init__(self):
        self.router = APIRouter(dependencies=[Depends(verify_api_key)])
        self.router.add_api_route("/HelloWorldApi/welcome", self.welcome, methods=["GET"])

    def welcome(self):
        return {
            "message": "Hello World!"
        }

hello_world_api = HelloWorldApi()
app.include_router(hello_world_api.router)
