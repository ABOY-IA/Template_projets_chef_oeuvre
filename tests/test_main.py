import pytest
import httpx
from unittest.mock import patch, MagicMock
from asgi_lifespan import LifespanManager
from api.main import app
from tests.utils.logger import logger


@pytest.fixture(autouse=True)
def mock_external_dependencies():
    with (
        patch("app.notify_discord.notify_discord") as mock_notify,
        patch("mlflow.start_run") as mock_start_run,
        patch("mlflow.log_param") as mock_log_param,
        patch("mlflow.log_metric") as mock_log_metric,
    ):
        mock_start_run.return_value.__enter__.return_value = MagicMock()
        mock_notify.return_value = None
        mock_log_param.return_value = None
        mock_log_metric.return_value = None
        yield


@pytest.mark.asyncio
async def test_health_check():
    logger.info("Début du test: test_health_check")
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    logger.success("Fin du test: test_health_check")


@pytest.mark.asyncio
async def test_predict_valid():
    logger.info("Début du test: test_predict_valid")
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/predict", json={"data": [1.0, 2.0, 3.0]}
            )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert abs(data["prediction"] - 2.0) < 1e-6
    logger.success("Fin du test: test_predict_valid")


@pytest.mark.asyncio
async def test_predict_empty_data():
    logger.info("Début du test: test_predict_empty_data")
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.post("/predict", json={"data": []})
    assert response.status_code == 400
    assert "Erreur lors de la prédiction" in response.text
    logger.success("Fin du test: test_predict_empty_data")


@pytest.mark.asyncio
async def test_generate():
    logger.info("Début du test: test_generate")
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/generate", json={"prompt": "test prompt"}
            )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "test prompt" in data["result"]
    logger.success("Fin du test: test_generate")


@pytest.mark.asyncio
async def test_retrain():
    logger.info("Début du test: test_retrain")
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.post("/retrain")
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == "Retrain déclenché (simulation)"
    logger.success("Fin du test: test_retrain")
