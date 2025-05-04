import pytest

def test_index(client):
    response = client.get('/')
    assert b"Welcome to Jack's Flask App" in response.data
    assert b"merc.png" in response.data

