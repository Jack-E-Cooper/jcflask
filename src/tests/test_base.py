import pytest

def test_index(client):
    response = client.get('/')
    assert b"Jack Cooper" in response.data
    assert b"Home" in response.data
    assert b"About" in response.data

