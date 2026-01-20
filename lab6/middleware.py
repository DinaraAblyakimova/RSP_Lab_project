from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from logger_config import logger
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"HTTP Request: {request.method} {request.url.path}")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(f"Error occurred: {e}")
            raise e

        duration = (time.time() - start_time) * 1000
        logger.info(f"HTTP Response: status={response.status_code} ({duration:.2f} ms)")
        return response
