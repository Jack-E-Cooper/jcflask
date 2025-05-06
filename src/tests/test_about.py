import pytest

page_url = '/about'

def test_header(client):
    response = client.get(page_url)
    assert b"About Me - John Cooper" in response.data

