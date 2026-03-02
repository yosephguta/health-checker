from datetime import datetime, timezone
from app.models import CheckResult
import httpx    

async def check_url(url: str, timeout: int = 5) -> CheckResult:
    try:
            
        time_now = datetime.now(timezone.utc)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
        time_after = datetime.now(timezone.utc)
        response_time_ms = (time_after - time_now).total_seconds() * 1000
        status = "up"
        status_code = response.status_code

        return CheckResult(
            url=url,
            status=status,
            status_code=status_code,
            response_time_ms=response_time_ms,
            checked_at=datetime.now(timezone.utc)
        )
    
    except httpx.RequestError:
        return CheckResult(
            url=url,
            status="down",
            status_code=None,
            response_time_ms=None,
            checked_at=datetime.now(timezone.utc)
    )