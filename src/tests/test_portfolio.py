import pytest

page_url = '/portfolio'

def test_header(client):
    response = client.get(page_url)
    assert b"My Projects" in response.data



