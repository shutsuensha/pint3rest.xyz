from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import time
import json
from app.logger import logger
from app.config import settings

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def client_http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Обработчик клиенских ошибок"""
        if settings.LOGGING_CLIENT_ERRORS:
            request_data = {
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host,
                "headers": dict(request.headers),
                "body": None
            }

            with open("app/logs/client_errors.log", "a", encoding="utf-8") as log_file:
                log_file.write(f"Client HTTP Error {exc.status_code}: {exc.detail}\n")
                log_file.write(f"Метод: {request_data['method']}\n")
                log_file.write(f"URL: {request_data['url']}\n")
                log_file.write(f"IP клиента: {request_data['client_ip']}\n")
                log_file.write(f"Заголовки: {json.dumps(request_data['headers'], ensure_ascii=False)}\n")
                log_file.write("-" * 80 + "\n")

        
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Обработчик неожиданных ошибок"""
        
        
        with open("app/logs/server_errors.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"Непредвиденная ошибка: {str(exc)}\n")

        return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})
