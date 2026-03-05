from fastapi import FastAPI
from app.models import CheckRequest, CheckResult, HealthResponse
from app.checker import check_url
import asyncio

app = FastAPI(
    title="URL Health Checker",
    version="1.0.0",
)

@app.get("/health")
async def health_check():
    return HealthResponse(status="healthy", version=app.version)

@app.post("/check", response_model=CheckResult)
async def check_url_endpoint(request: CheckRequest):
    return await check_url(request.url, request.timeout)

@app.post("/check/batch", response_model=list[CheckResult])
async def check_urls_batch(requests: list[CheckRequest]):
    responses = await asyncio.gather(*[check_url(request.url, request.timeout) for request in requests])
    return responses
 