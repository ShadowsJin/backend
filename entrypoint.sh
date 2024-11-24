alembic upgrade head # apply migrations
# variable for correct multiworkers gunicorn metrics scrapping
mkdir -p prometheus-multiprocess
export PROMETHEUS_MULTIPROC_DIR=$(pwd)/prometheus-multiprocess
# start fastapi app
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind="0.0.0.0:${FASTAPI_PORT}"
