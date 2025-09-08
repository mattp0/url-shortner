from __future__ import annotations

from fastapi import FastAPI

from urlshortner.api.routers import health
from urlshortner.core.config import get_settings

app = FastAPI(title="urlshortner API")

# routers
app.include_router(health.router)

@app.get("/")
async def root():
    s = get_settings()
    return {"service": "urlshortner", "env": s.ENV, "status": "ok"}