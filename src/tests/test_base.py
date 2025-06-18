import pytest
from bs4 import BeautifulSoup


# Define a test for each route that should have a specific nav item active.
@pytest.mark.parametrize(
    "url, expected_active_text",
    [
        ("/", "Home"),
        ("/about", "About"),
        ("/portfolio", "Portfolio"),
        ("/blog", "Blog"),
        ("/contact", "Contact"),
    ],
)
def test_navigation_active(client, url, expected_active_text, app):
    if url == "/blog" and not app.config.get("ENABLE_BLOG", False):
        pytest.skip("Blog feature is disabled (ENABLE_BLOG is False)")
    response = client.get(url)
    assert (
        response.status_code == 200
    ), f"GET {url} failed with status code {response.status_code}"
    html = response.get_data(as_text=True)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find the navigation bar and all nav-link anchors
    nav = soup.find("nav")
    nav_links = nav.find_all("a", class_="nav-link")

    # Find the a tags with the active class
    active_links = [link for link in nav_links if "active" in link.get("class", [])]
    assert (
        len(active_links) == 1
    ), f"Expected exactly one active nav link on {url}, but found {len(active_links)}"

    # Check that the active nav link’s text matches the expected text.
    active_item_text = active_links[0].get_text(strip=True)
    assert expected_active_text in active_item_text, (
        f"For URL {url}, expected nav item text '{expected_active_text}' to be active, "
        f"but got '{active_item_text}'"
    )


@pytest.mark.parametrize(
    "url",
    [
        ("/"),
        ("/about"),
        ("/portfolio"),
        ("/blog"),
        ("/contact"),
    ],
)
def test_header_has_linkedin_github(client, url, app):
    if url == "/blog" and not app.config.get("ENABLE_BLOG", False):
        pytest.skip("Blog feature is disabled (ENABLE_BLOG is False)")
    response = client.get(url)
    assert (
        response.status_code == 200
    ), f"GET {url} failed with status code {response.status_code}"

    html = response.get_data(as_text=True)
    soup = BeautifulSoup(html, "html.parser")
    nav = soup.find("nav")
    assert nav is not None

    # Check for GitHub icon/link
    github_link = nav.find("a", href="https://github.com/Jack-E-Cooper")
    assert github_link is not None, "GitHub link not found in navbar"
    assert github_link.find("i", class_="fab fa-github") is not None, "GitHub icon not found in navbar"

    # Check for LinkedIn icon/link
    linkedin_link = nav.find("a", href="https://linkedin.com/in/johnedwardcooper")
    assert linkedin_link is not None, "LinkedIn link not found in navbar"
    assert linkedin_link.find("i", class_="fab fa-linkedin") is not None, "LinkedIn icon not found in navbar"
