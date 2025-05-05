import pytest

def test_home(client):
    response = client.get('/')
    assert b"Welcome to John Cooper's Portfolio" in response.data
    assert b"merc.png" in response.data
