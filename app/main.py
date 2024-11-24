from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.logger import logger
from app.routers.quizes import router as quizes_router
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    instrumentator.expose(app, tags=['metrics'])
    yield


app = FastAPI(root_path='/api', lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f'http://localhost:{settings.FRONTEND_PORT}', 'http://localhost'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=['/metrics', '/docs', '/openapi.json']
).instrument(app, latency_lowr_buckets=(0.1, 0.25, 0.5, 0.75, 1))


@app.middleware('http')
async def logging(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(exc.message, extra={'endpoint': f'{request.method} {request.url.path}'})
        return Response(content='Internal Server Error', status_code=500)


for router in [users_router, quizes_router]:
    app.include_router(router)
