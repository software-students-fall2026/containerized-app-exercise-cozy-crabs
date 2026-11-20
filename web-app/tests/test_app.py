"""Placeholder tests for the web app"""

from app import app


def test_index():
    """The home page should load and say 'Hello, world!'"""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert (
        b"Hello" in response.data
    )  # The 'b' converts it to a bytes-like object so the test works properly
