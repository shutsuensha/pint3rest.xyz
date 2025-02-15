import time
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.logger import logger


async def log_requests_and_server_http_exception_handler(request: Request, call_next):
    """Логирование входящих запросов с измерением времени выполнения и обработка ошибок сервера в обработке запросов"""
    start_time = time.time()  # Засекаем время начала запроса
    
    try:
        response: Response = await call_next(request)
        elapsed_time = time.time() - start_time  # Вычисляем время выполнения
        
        # Запись в файл
        with open("app/logs/requests.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"{request.method} {request.url} {request.client.host} | Status: {response.status_code} | Time: {elapsed_time:.4f} сек.\n")

        return response
    except Exception as e:
        elapsed_time = time.time() - start_time  # Записываем время даже в случае ошибки
        logger.error(f"Ошибка при обработке запроса {request.method} {request.url} {request.client.host} : {e}", exc_info=True)

        with open("app/logs/requests.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"{request.method} {request.url} {request.client.host} | Status: ERROR | Time: {elapsed_time:.4f} сек. | Error: {e}\n")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )


def register_middleware(app: FastAPI):
    """Регистрация middleware."""
    app.middleware("http")(log_requests_and_server_http_exception_handler)  # Логирование всех HTTP-запросов

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"],
    )
