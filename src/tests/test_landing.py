import pytest

def test_index(client):
    response = client.get('/')
    assert b"Welcome to Jack's Flask App" in response.data
    assert b"merc.png" in response.data

def test_landing_navbar(client, nav_bar_contents):
    response = client.get('/')
    for item in nav_bar_contents:
        assert item in response.data

