import pytest
from unittest.mock import AsyncMock, patch
from app.checker import check_url
import httpx

@pytest.mark.asyncio
async def test_check_url_success():
    mock_response = AsyncMock()
    mock_response.status_code = 200

    with patch("app.checker.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        result = await check_url("https://google.com")

    assert result.status == "up"
    assert result.status_code == 200
    assert result.response_time_ms is not None

@pytest.mark.asyncio
async def test_check_url_down():
    with patch("app.checker.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
        side_effect=httpx.RequestError("Network error")
        )
        result = await check_url("https://google.com")
        assert result.status == "down"
        assert result.status_code is None
        assert result.response_time_ms is None

@pytest.mark.asyncio
async def test_check_url_timeout():
    with patch("app.checker.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            side_effect=httpx.TimeoutException("Request timed out")
        )
        result = await check_url("https://google.com")
        assert result.status == "down"
        assert result.status_code is None
        assert result.response_time_ms is None
        

