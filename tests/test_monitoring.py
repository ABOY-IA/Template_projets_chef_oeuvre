import pytest
from utils.logger import logger


@pytest.mark.asyncio
async def test_health_check(async_client):
    logger.info("Début du test: test_health_check")
    resp = await async_client.get("/health")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"status": "ok"}
    logger.success("Fin du test: test_health_check")
