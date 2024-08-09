from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f'http://localhost:{settings.FRONTEND_PORT}'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
