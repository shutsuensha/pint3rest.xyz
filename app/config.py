from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEV_MODE: bool

    SENTRY_DSN: str

    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: int
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASS: str
    POSTGRES_DB_NAME: str

    TEST_POSTGRES_DB_HOST: str
    TEST_POSTGRES_DB_PORT: int
    TEST_POSTGRES_DB_USER: str
    TEST_POSTGRES_DB_PASS: str
    TEST_POSTGRES_DB_NAME: str

    MONGO_DB_HOST: str
    MONGO_DB_PORT: int
    MONGO_DB_USER: str
    MONGO_DB_PASS: str
    MONGO_DB_NAME: str

    MYSQL_DB_HOST: str
    MYSQL_DB_PORT: int
    MYSQL_DB_USER: str
    MYSQL_DB_PASS: str
    MYSQL_DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASS: str
    REDIS_DB_REVOKE_TOKENS: int
    REDIS_DB_CACHE: int
    REDIS_DB_CELERY_BROKER: int
    REDIS_DB_CELERY_RESULT: int
    REDIS_DB_CELERY_REDBEAT: int
    REDIS_DB_LIMITER: int

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool

    API_DOMAIN: str
    TRUSTED_HOST: str
    FRONTEND_DOMAIN: str
    TRUSTED_ORIGIN: str

    LOGGING_CLIENT_ERRORS: bool
    LOGGING_REQUESTS: bool

    LOGS_PATH: str
    MEDIA_PATH: str

    YANDEX_STORAGE_KEY: str
    YANDEX_STORAGE_SECRET_KEY: str
    YANDEX_STORAGE_BUCKET: str

    GOOGLE_OAUTH2_CLIENT_ID: str
    GOOGLE_OAUTH2_CLIENT_SECRET: str
    GOOGLE_OAUTH2_REDIRECT_URI: str

    PATH_VIDEO_STREAM: str

    @property
    def RABBITMQ_URL_BROKER(self):
        return f"pyamqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"

    @property
    def RABBITMQ_URL_RESULT(self):
        return f"rpc://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"

    @property
    def MYSQL_URL_ASYNC(self):
        return f"mysql+aiomysql://{self.MYSQL_DB_USER}:{self.MYSQL_DB_PASS}@{self.MYSQL_DB_HOST}:{self.MYSQL_DB_PORT}/{self.MYSQL_DB_NAME}"

    @property
    def MONGO_URL(self):
        return f"mongodb://{self.MONGO_DB_USER}:{self.MONGO_DB_PASS}@{self.MONGO_DB_HOST}:{self.MONGO_DB_PORT}/{self.MONGO_DB_NAME}?authSource=admin"

    @property
    def REDIS_URL_CELERY_REDBEAT(self):
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_CELERY_REDBEAT}"

    @property
    def REDIS_URL_CELERY_BROKER(self):
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_CELERY_BROKER}"

    @property
    def REDIS_URL_CELERY_RESULT(self):
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_CELERY_RESULT}"

    @property
    def REDIS_URL_REVOKE_TOKENS(self):
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_REVOKE_TOKENS}"

    @property
    def REDIS_URL_CACHE(self):
        return (
            f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_CACHE}"
        )

    @property
    def REDIS_URL_LIMITER(self):
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_LIMITER}"

    @property
    def POSTGRES_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASS}@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}"

    @property
    def TEST_POSTGRES_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.TEST_POSTGRES_DB_USER}:{self.TEST_POSTGRES_DB_PASS}@{self.TEST_POSTGRES_DB_HOST}:{self.TEST_POSTGRES_DB_PORT}/{self.TEST_POSTGRES_DB_NAME}"

    @property
    def POSTGRES_URL_SYNC(self):
        return f"postgresql://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASS}@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
