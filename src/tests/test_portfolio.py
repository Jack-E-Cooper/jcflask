import pytest
from bs4 import BeautifulSoup

page_url = "/portfolio"


def test_header(client):
    response = client.get(page_url)
    assert b"My Projects" in response.data


def test_project_cards_present(client, app):
    response = client.get(page_url)
    soup = BeautifulSoup(response.data, "html.parser")
    cards = soup.select(".card .card-title")
    assert len(cards) > 0
    # Check that each card displays a title and summary from the centralized project list
    from jcflask.project import get_portfolio_projects

    project_titles = {p["title"] for p in get_portfolio_projects()}
    found_titles = {card.text.strip() for card in cards}
    assert project_titles & found_titles, "At least one known project title should be present in the cards"


def test_project_image_url_env(client, app):
    from jcflask.project import get_portfolio_projects
    import os

    # Test for development environment (should use url_for/static)
    app.config["ENV"] = "development"
    with app.app_context():
        projects = get_portfolio_projects()
        for project in projects:
            assert project["image"].startswith("/static/") or "/static/" in project["image"], \
                f"Expected local static image path in development, got: {project['image']}"

    # Test for production environment (should use prod_image_url)
    app.config["ENV"] = "production"
    with app.app_context():
        projects = get_portfolio_projects()
        for project in projects:
            assert project["image"].startswith("http"), \
                f"Expected remote image URL in production, got: {project['image']}"

