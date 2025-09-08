from __future__ import annotations

from fastapi import APIRouter, HTTPException
import redis

from urlshortner.core.config import get_settings
from urlshortner.core.db.session import db_ready

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz():
    return {"ok": True}


@router.get("/readyz")
async def readyz():
    # DB readiness
    try:
        await db_ready()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"db not ready: {e!s}")

    # Redis readiness (if configured)
    settings = get_settings()
    if settings.REDIS_URL:
        try:
            r = redis.Redis.from_url(settings.REDIS_URL)
            if not r.ping():
                raise RuntimeError("redis ping failed")
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=503, detail=f"redis not ready: {e!s}")

    return {"ok": True}
