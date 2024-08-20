from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.quizes import router as quizes_router
from app.routers.users import router as users_router

app = FastAPI(root_path='/api')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f'http://localhost:{settings.FRONTEND_PORT}'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

for router in [users_router, quizes_router]:
    app.include_router(router)
