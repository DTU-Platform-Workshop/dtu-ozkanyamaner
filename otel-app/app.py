import signal
import sys
import os

from fastapi import FastAPI
from contextlib import asynccontextmanager
from opentelemetry import trace

from telemetry import instrument_app, setup_tracer

setup_tracer("otel-app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"I'm alive at {os.getenv('PORT', '4242')}", flush=True)
    yield
    print(f"I'm shutting down", flush=True)


app = FastAPI(title="my-app", lifespan=lifespan)
instrument_app(app)


@app.get("/readyz")
@app.get("/livez")
@app.get("/")
def hello():
    return f"Hello World!"


def terminate(signal, frame):
    sys.exit(0)


if __name__ == "__main__":
    import uvicorn
    
    # Workaround for Python not always respecting sigterm
    signal.signal(signal.SIGTERM, terminate)

    port = int(os.getenv("PORT", "4242"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
