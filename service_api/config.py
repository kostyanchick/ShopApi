import os


class BaseConfig:
    APP_HOST = os.getenv('APP_HOST', 'localhost')
    APP_PORT = os.getenv('APP_PORT', 8080)
    SERVICE_NAME = os.getenv('SERVICE_NAME', 'shop_api')
    SECRET_KEY = os.getenv('SECRET_KEY', 'this-should-be-secret')
    DEBUG = True
    PG_HOST = os.getenv('PG_HOST', 'localhost')
    # 54321 port used for postgres service in docker-compose.yml
    PG_PORT = os.getenv('PG_PORT', 54321)
    PG_USER = os.getenv('PG_USER', 'postgres')
    PG_PW = os.getenv('PG_PASSWORD', '')
    PG_DB_NAME = os.getenv('DB_NAME', 'shop_dev')
    PG_DATABASE_URL = os.getenv('DATABASE_URL',
                                f'postgresql://{PG_USER}:{PG_PW}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}')


class ProdConfig(BaseConfig):
    DEBUG = False
