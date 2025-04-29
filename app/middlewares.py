import json
import time

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sentry_sdk import capture_exception, capture_message

from app.config import settings
from app.logger import logger, requests_logger


async def log_requests_and_server_http_exception_handler(request: Request, call_next):
    """Логирование входящих запросов с измерением времени выполнения и обработка ошибок сервера в обработке запросов"""

    start_time = time.time()  # Засекаем время начала запроса

    try:
        response: Response = await call_next(request)
        elapsed_time = time.time() - start_time  # Вычисляем время выполнения

        # Запись в файл в формате JSONL
        if settings.LOGGING_REQUESTS:
            log_data = {
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host,
                "status_code": response.status_code,
                "elapsed_time": round(elapsed_time, 4),
            }

            requests_logger.info(json.dumps(log_data, ensure_ascii=False))

            capture_message(json.dumps(log_data, ensure_ascii=False))

        return response
    except Exception as e:
        elapsed_time = time.time() - start_time  # Записываем время даже в случае ошибки
        logger.error(
            f"Ошибка при обработке запроса {request.method} {request.url} {request.client.host} : {e}",
            exc_info=True,
        )

        capture_exception(e)

        if settings.LOGGING_REQUESTS:
            log_data = {
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host,
                "status_code": "ERROR",
                "elapsed_time": round(elapsed_time, 4),
                "error": str(e),
            }

            requests_logger.info(json.dumps(log_data, ensure_ascii=False))

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )


def register_middleware(app: FastAPI):
    """Регистрация middleware."""
    app.middleware("http")(log_requests_and_server_http_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],
    )
