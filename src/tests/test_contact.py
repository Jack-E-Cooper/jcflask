import pytest

page_url = '/contact'

def test_header(client):
    response = client.get(page_url)
    assert b"Contact" in response.data

def test_contact_form_display(client):
    response = client.get(page_url)
    assert response.status_code == 200
    assert b'<form' in response.data
    assert b'name="name"' in response.data
    assert b'name="email"' in response.data
    assert b'name="message"' in response.data
    assert b'action="https://formspree.io/f/myzwwkdd"' in response.data

