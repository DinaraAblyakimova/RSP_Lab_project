from fastapi import FastAPI, HTTPException
from logger_config import logger
from middleware import LoggingMiddleware
from decorators import log_execution_time
import asyncio

app = FastAPI()
app.add_middleware(LoggingMiddleware)

@app.get("/hello")
async def say_hello():
    logger.info("Handling /hello request")
    return {"message": "Hello, World!"}

@app.get("/log")
async def log_example():
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARN message")
    logger.error("This is an ERROR message")
    return {"status": "Check logs for details!"}

@app.get("/testError")
async def test_error():
    raise HTTPException(status_code=500, detail="Simulated error")

@app.get("/time")
@log_execution_time
async def execution_time():
    await asyncio.sleep(0.5)  # симуляция долгого метода
    return {"message": "Method execution completed"}
