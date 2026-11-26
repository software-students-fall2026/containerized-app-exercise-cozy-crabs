"""Shared fixtures for database integration tests"""

import pytest
import database


@pytest.fixture
def test_db(monkeypatch):
    """Connect to a real MongoDB test database"""
    uri = "mongodb://localhost:27017/voiceproject_web_test"

    monkeypatch.setenv("MONGO_URI", uri)
    database.get_client.cache_clear()

    db = database.get_db()

    # Start each test with an empty collection
    db[database.COLLECTION].delete_many({})

    yield db

    # Clean up after the test
    db[database.COLLECTION].delete_many({})
    database.get_client(uri).close()
    database.get_client.cache_clear()