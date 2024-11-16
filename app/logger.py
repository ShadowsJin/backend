import logging
from app.config import settings
from datetime import datetime
from clickhouse_connect import get_client


class ClickHouseHandler(logging.Handler):
    def __init__(self):
        self.client = None
        self.init_clickhouse()
        super().__init__()

    def init_clickhouse(self):
        client = get_client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            username=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            database=settings.CLICKHOUSE_DB
        )
        self.client = client
        client.command('DROP TABLE IF EXISTS logs_fastapi')
        # location = file and line
        client.command('''
                CREATE TABLE logs_fastapi (
                    timestamp DateTime,
                    level String,
                    service String,
                    message String,
                    endpoint String
                    -- location Nullable(String)
                )
                ENGINE MergeTree
                PARTITION BY toYYYYMMDD(timestamp)
                ORDER BY timestamp
            ''')

    def emit(self, record):
        # print(record.__dict__)
        self.client.insert(
            'logs_fastapi',
            [[
                datetime.now(),
                record.levelname,
                record.name,
                record.msg,
                record.endpoint
            ]],
            column_names=['timestamp', 'level', 'service', 'message', 'endpoint']
        )


logger = logging.Logger(name='fastapi logger', level=logging.INFO)
logger.addHandler(ClickHouseHandler())
