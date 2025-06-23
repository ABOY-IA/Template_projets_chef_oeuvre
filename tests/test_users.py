import os
import sys
import pytest
from tests.utils.logger import logger

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_create_user(async_client):
    logger.info("Début du test: test_create_user")
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }
    resp = await async_client.post("/users/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert data["role"] == "user"
    logger.success("Fin du test: test_create_user")


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_login_user_returns_tokens(async_client):
    logger.info("Début du test: test_login_user_returns_tokens")
    await async_client.post(
        "/users/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "pwd1234",
        },
    )
    resp = await async_client.post(
        "/users/login", json={"username": "loginuser", "password": "pwd1234"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["access_token"], str)
    assert isinstance(data["refresh_token"], str)
    assert data["token_type"] == "bearer"
    logger.success("Fin du test: test_login_user_returns_tokens")
