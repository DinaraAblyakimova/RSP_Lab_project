import time
from logger_config import logger

def log_execution_time(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = (time.time() - start) * 1000
        logger.info(f"{func.__name__} executed in {end:.2f} ms")
        return result
    return wrapper
