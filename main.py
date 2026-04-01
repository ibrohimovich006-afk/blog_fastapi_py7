from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api import api_router

app = FastAPI(title='Blog App API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router)

BASE_DIR = Path(__file__).resolve().parent


@app.get('/')
def home():
    return FileResponse(BASE_DIR / 'index.html')
