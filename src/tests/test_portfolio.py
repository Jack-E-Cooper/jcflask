import pytest
from bs4 import BeautifulSoup

page_url = '/portfolio'

def test_header(client):
    response = client.get(page_url)
    assert b"My Projects" in response.data

def test_project_cards_present(client):
    response = client.get(page_url)
    soup = BeautifulSoup(response.data, "html.parser")
    cards = soup.select('.card-title')
    assert len(cards) > 0
    # Check that at least one known project is present
    assert any("Personal Website" in card.text for card in cards)

# def test_project_links_work(client):
#     response = client.get(page_url)
#     soup = BeautifulSoup(response.data, "html.parser")
#     links = soup.select('a.btn-outline-primary')
#     assert links
#     for link in links:
#         href = link.get('href')
#         project_response = client.get(href)
#         assert project_response.status_code == 200
#         assert b"Project" in project_response.data or b"Personal Website" in project_response.data



