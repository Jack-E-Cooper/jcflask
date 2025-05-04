import pytest

page_url = '/about'

def test_header(client):
    response = client.get(page_url)
    assert b"About this App" in response.data

def test_about_navbar(client, nav_bar_contents):
    response = client.get(page_url)
    for item in nav_bar_contents:
        assert item in response.data

