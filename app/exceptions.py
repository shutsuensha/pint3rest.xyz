import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.logger import logger, client_errors_logger

from sentry_sdk import capture_exception


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def client_http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Обработчик клиентских ошибок"""

        # Логирование ошибок клиента, если включено в настройках
        if settings.LOGGING_CLIENT_ERRORS:
            # Подготовка данных запроса для логирования
            request_data = {
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host,
                "headers": dict(request.headers),
                "body": None,  # Можно добавить тело запроса, если оно необходимо
                "status_code": exc.status_code,
                "detail": exc.detail,
            }

            # Логирование ошибки с использованием client_errors_logger
            client_errors_logger.warning(json.dumps(request_data, ensure_ascii=False))

            # Регистрация ошибки в Sentry
            capture_exception(exc, level="warning", extra=request_data)


        # Возврат клиенту с ошибкой
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Обработчик неожиданных ошибок"""

        logger.error(f"Непредвиденная ошибка: {str(exc)}\n")

        capture_exception(exc)

        return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})
