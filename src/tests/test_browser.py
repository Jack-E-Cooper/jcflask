import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from jcflask.db import db
from jcflask.models import BlogPost
import time
import logging

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(autouse=True)
def reset_database(app):
    """Initialize a new database for each test."""
    with app.app_context():
        db.drop_all()  # Drop all tables
        db.create_all()  # Recreate all tables
        db.session.commit()


@pytest.fixture
def browser():
    """Fixture to initialize and quit the browser."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    yield driver
    driver.quit()


def test_new_post_button(browser, live_server):
    """Test the 'New Post' button functionality."""
    live_server_url = live_server.url().rstrip("/")
    browser.get(f"{live_server_url}/admin/posts")

    new_post_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Create New Post"))
    )
    new_post_button.click()

    assert "Create Post" in browser.title
    assert browser.current_url.rstrip("/") == f"{live_server_url}/admin/posts/new"


def test_create_post_with_markdown(browser, live_server):
    """Test creating a new post with Markdown content."""
    logging.debug("Starting test_create_post_with_markdown")
    live_server_url = live_server.url().rstrip("/")  # Ensure consistent URL formatting
    browser.get(f"{live_server_url}/admin/posts/new")

    unique_title = f"Markdown Test Post {int(time.time())}"
    browser.find_element(By.ID, "title").send_keys(unique_title)

    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys(
        "# Markdown Title\n\nThis is a **Markdown** post."
    ).perform()

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    # Verify the post request was sent by checking the page source or resulting state
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Post created successfully!')]")
        )
    )
    assert "Post created successfully!" in browser.page_source

    browser.get(f"{live_server_url}/blog")
    assert unique_title in browser.page_source
    assert "<h1>Markdown Title</h1>" in browser.page_source
    assert "<p>This is a <strong>Markdown</strong> post.</p>" in browser.page_source


def test_create_post_with_empty_markdown(browser, live_server):
    """Test creating a post with an empty Markdown editor."""
    live_server_url = live_server.url()
    browser.get(f"{live_server_url}/admin/posts/new")

    browser.find_element(By.ID, "title").send_keys("Empty Markdown Test")

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    content_error = browser.find_element(By.ID, "content-error")
    assert content_error.is_displayed()
    assert content_error.text == "Content cannot be empty."


def test_edit_post(browser, live_server):
    """Test editing an existing post."""
    live_server_url = live_server.url()

    unique_title = f"Test Post {int(time.time())}"
    browser.get(f"{live_server_url}/admin/posts/new")
    assert (
        browser.current_url.rstrip("/") == f"{live_server_url}/admin/posts/new"
    )  # Verify URL before interacting

    browser.find_element(By.ID, "title").send_keys(unique_title)
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys(
        "This is a test post."
    ).perform()

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    browser.get(f"{live_server_url}/admin/posts")
    assert (
        browser.current_url.rstrip("/") == f"{live_server_url}/admin/posts"
    )  # Verify URL before interacting

    # Ensure the unique title is present in the page source before accessing the element
    assert unique_title in browser.page_source

    # Access the row containing the unique title and locate the edit button
    post_row = browser.find_element(
        By.XPATH, f"//tr[td[contains(text(), '{unique_title}')]]"
    )
    edit_button = post_row.find_element(By.CSS_SELECTOR, "a.btn.btn-secondary")
    post_id = edit_button.get_attribute("href").split("/")[-2]
    edit_button.click()

    assert (
        browser.current_url == f"{live_server_url}/admin/posts/{post_id}/edit"
    )  # Verify URL before interacting

    browser.find_element(By.ID, "title").clear()
    browser.find_element(By.ID, "title").send_keys("Updated Test Post")
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys(
        "This is an updated test post."
    ).perform()

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    assert browser.current_url == f"{live_server_url}/admin/posts"
    assert "Post updated successfully!" in browser.page_source


def test_edit_post_with_markdown(browser, live_server):
    """Test editing a post with Markdown content."""
    live_server_url = live_server.url()

    unique_title = f"Original Markdown Post {int(time.time())}"
    browser.get(f"{live_server_url}/admin/posts/new")
    browser.find_element(By.ID, "title").send_keys(unique_title)
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys(
        "# Original Title\n\nOriginal **content**."
    ).perform()

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    browser.get(f"{live_server_url}/admin/posts")
    # Wait for the table containing posts to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    assert unique_title in browser.page_source

    edit_button = browser.find_element(
        By.XPATH, f"//tr[td[contains(text(), '{unique_title}')]]/td/a"
    )
    edit_button.click()

    browser.find_element(By.ID, "title").clear()
    browser.find_element(By.ID, "title").send_keys("Updated Markdown Post")
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys(
        "\b" * 50 + "# Updated Title\n\nUpdated **content**."
    ).perform()

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    browser.get(f"{live_server_url}/blog")
    assert "Updated Markdown Post" in browser.page_source
    assert "<h1>Updated Title</h1>" in browser.page_source
    assert "<p>Updated <strong>content</strong>.</p>" in browser.page_source


def test_delete_post(browser, live_server):
    """Test deleting a post."""
    live_server_url = live_server.url()

    unique_title = f"Test Post {int(time.time())}"
    browser.get(f"{live_server_url}/admin/posts/new")
    browser.find_element(By.ID, "title").send_keys(unique_title)
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys(
        "This is a test post."
    ).perform()

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    browser.get(f"{live_server_url}/admin/posts")
    # Wait for the table containing posts to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    assert unique_title in browser.page_source

    post_row = browser.find_element(
        By.XPATH, f"//tr[td[contains(text(), '{unique_title}')]]"
    )
    delete_button = post_row.find_element(By.CSS_SELECTOR, "button.btn-danger")
    delete_button.click()

    alert = WebDriverWait(browser, 2).until(EC.alert_is_present())
    assert alert.text == "Are you sure you want to delete this post?"
    alert.accept()

    assert browser.current_url == f"{live_server_url}/admin/posts"
    assert "Post deleted successfully!" in browser.page_source


def test_create_post_empty_title(browser, live_server):
    """Test form validation when creating a post with an empty title."""
    live_server_url = live_server.url()
    browser.get(f"{live_server_url}/admin/posts/new")

    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys(
        "This is a test post."
    ).perform()

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    title_error = browser.find_element(By.ID, "title-error")
    assert title_error.is_displayed()
    assert title_error.text == "Title cannot be empty."


def test_edit_post_empty_content(browser, live_server):
    """Test form validation when editing a post with empty content."""
    live_server_url = live_server.url()

    unique_title = f"Test Post {int(time.time())}"
    browser.get(f"{live_server_url}/admin/posts/new")
    browser.find_element(By.ID, "title").send_keys(unique_title)
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys(
        "This is a test post."
    ).perform()

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    browser.get(f"{live_server_url}/admin/posts")
    # Wait for the table containing posts to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    assert unique_title in browser.page_source

    edit_button = browser.find_element(
        By.XPATH, f"//tr[td[contains(text(), '{unique_title}')]]/td/a"
    )
    edit_button.click()

    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys(
        "\b" * 50
    ).perform()

    # Use JavaScript to click the submit button
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    content_error = browser.find_element(By.ID, "content-error")
    assert content_error.is_displayed()
    assert content_error.text == "Content cannot be empty."


def test_portfolio_project_links(browser, live_server):
    """Test that project links on the portfolio page work and load dynamic content."""
    live_server_url = live_server.url().rstrip("/")
    browser.get(f"{live_server_url}/portfolio")
    # Find all project "View Project" buttons
    project_buttons = browser.find_elements(By.CSS_SELECTOR, "a.btn-outline-primary")
    assert project_buttons
    # Click the first project button
    project_buttons[0].click()
    # Wait for the project page to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    # Check for expected content on the project page
    assert "Personal Website" in browser.page_source or "Project" in browser.page_source
    assert "Description" in browser.page_source
    assert "Technologies Used" in browser.page_source


def test_project_page_direct_access(browser, live_server):
    """Test direct access to a project page shows dynamic content."""
    live_server_url = live_server.url().rstrip("/")
    browser.get(f"{live_server_url}/project/flaskwebapp")
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Personal Website" in browser.page_source
    assert "Description" in browser.page_source
    assert "Technologies Used" in browser.page_source
