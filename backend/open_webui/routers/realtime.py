import aiohttp
import logging

from fastapi import APIRouter, Depends, HTTPException, Request

from open_webui.utils.auth import get_verified_user

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/session")
async def create_realtime_session(request: Request, user=Depends(get_verified_user)):
    idx = 0
    url = request.app.state.config.OPENAI_API_BASE_URLS[idx]
    key = request.app.state.config.OPENAI_API_KEYS[idx]
    session = None
    try:
        session = aiohttp.ClientSession(trust_env=True)
        r = await session.post(
            f"{url}/realtime/sessions",
            json={"model": "gpt-4o-realtime-preview", "voice": "verse"},
            headers={"Authorization": f"Bearer {key}"},
        )
        data = await r.json()
        if r.status >= 400:
            raise HTTPException(status_code=r.status, detail=data)
        return data
    except Exception as e:  # pragma: no cover - network errors
        log.exception(e)
        raise HTTPException(status_code=500, detail="Realtime session error")
    finally:
        if session:
            await session.close()
