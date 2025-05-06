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
    ]
)
def test_navigation_active(client, url, expected_active_text):
    response = client.get(url)
    assert response.status_code == 200, f"GET {url} failed with status code {response.status_code}"
    html = response.get_data(as_text=True)
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the navigation bar and all nav items
    nav = soup.find("nav")
    nav_items = nav.find_all("li", class_="nav-item")
    
    # Find the li tags with the active class
    active_items = [item for item in nav_items if "active" in item.get("class", [])]
    assert len(active_items) == 1, f"Expected exactly one active nav item on {url}, but found {len(active_items)}"
    
    # Check that the active nav item’s link text matches the expected text.
    active_anchor = active_items[0].find("a")
    active_item_text = active_anchor.get_text(strip=True)
    assert expected_active_text in active_item_text, (
        f"For URL {url}, expected nav item text '{expected_active_text}' to be active, "
        f"but got '{active_item_text}'"
    )