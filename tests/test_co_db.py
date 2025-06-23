import os
import sys
import pytest
from api.db.session import connect_to_db
from tests.utils.logger import logger

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


@pytest.mark.asyncio
async def test_database_connection_does_not_fail():
    try:
        await connect_to_db()
    except Exception as e:
        logger.error(f"Échec de la connexion à la DB : {e}")
        pytest.fail(f"Échec de la connexion à la DB : {e}")
