import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_gallery_page_loads(client):
    """Test that the gallery page loads successfully."""
    response = client.get("/gallery/")
    assert response.status_code == 200
    assert b"Photo Gallery" in response.data

def test_gallery_images_present(client):
    """Test that gallery images are present in the HTML."""
    response = client.get("/gallery/")
    # Check for known image filenames in the gallery
    assert b"DTKT_speak_lead_grow.png" in response.data
    assert b"RES_presentation1.jpg" in response.data
    assert b"mil_1.jpg" in response.data
    assert b"mil_2.jpg" in response.data

def test_gallery_image_alt_texts(client):
    """Test that alt texts for images are present."""
    response = client.get("/gallery/")
    assert b'alt="Toastmasters Presentation 2017"' in response.data
    assert b'alt="Presentation to Rotary Youth for Peace 2025"' in response.data
    assert b'alt="Military Medal Parade"' in response.data
    assert b'alt="Iron Warrior"' in response.data

