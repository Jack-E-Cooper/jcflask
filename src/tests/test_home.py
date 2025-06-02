import pytest


def test_home(client):
    response = client.get("/")
    assert b"LinkedIn" in response.data
    assert b"github" in response.data
    assert b"JackCooperPortrait.jpg" in response.data
