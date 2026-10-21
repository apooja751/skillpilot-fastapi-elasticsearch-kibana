
import logging
import json
import os
import socket
import sys
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for key in ("method", "path", "status_code"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        return json.dumps(log_entry)


class LogstashTCPHandler(logging.Handler):
    def emit(self, record):
        try:
            message = self.format(record) + "\n"
            with socket.create_connection(
                (os.getenv("LOGSTASH_HOST", "localhost"),
                 int(os.getenv("LOGSTASH_PORT", "5000"))),
                timeout=2,
            ) as connection:
                connection.sendall(message.encode("utf-8"))
        except OSError:
            # Keep the application running if Logstash is unavailable.
            pass


app = FastAPI(title="SkillPilot FastAPI Logging")

logger = logging.getLogger("skillpilot")
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.propagate = False

formatter = JSONFormatter()

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logstash_handler = LogstashTCPHandler()
logstash_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(logstash_handler)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(
        "HTTP request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
        },
    )
    return response


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "SkillPilot FastAPI Logging is running"}


@app.get("/health")
async def health():
    logger.info("Health check requested")
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    logger.info("Item requested: %s", item_id)
    return {"item_id": item_id, "status": "success"}


@app.get("/error-demo")
async def error_demo():
    logger.error("Demonstration error log")
    return JSONResponse(
        status_code=500,
        content={"detail": "Demonstration error for log testing"},
    )
