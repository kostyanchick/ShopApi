from flask import Flask

from service_api.config import BaseConfig
from service_api.db import PGConnection

app = Flask(__name__)

app.config.from_object(BaseConfig)
pg_conn = PGConnection(pg_url=app.config.get('PG_DATABASE_URL'))
# initial set up
pg_conn.create_all_tables()
