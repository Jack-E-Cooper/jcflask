import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    """Fixture to initialize and quit the browser."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"  # Update this path if Chrome is installed elsewhere
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_new_post_button(browser, live_server):
    """Test the 'New Post' button functionality."""
    # Ensure the live server is running and get its URL
    live_server_url = live_server.url().rstrip("/")  # Normalize URL by removing trailing slash
    assert isinstance(live_server_url, str), "Live server URL must be a string"
    assert live_server_url.startswith("http://"), "Live server URL must start with http://"

    # Navigate to the admin posts page
    browser.get(f"{live_server_url}/admin/posts")

    # Find and click the "New Post" button
    new_post_button = browser.find_element(By.LINK_TEXT, "Create New Post")
    new_post_button.click()

    # Verify that the browser navigates to the "Create Post" page
    assert "Create Post" in browser.title
    assert browser.current_url.rstrip("/") == f"{live_server_url}/admin/posts/new"  # Normalize and compare URLs

def test_create_post_with_markdown(browser, live_server):
    """Test creating a new post with Markdown content."""
    live_server_url = live_server.url()
    browser.get(f"{live_server_url}/admin/posts/new")

    # Fill out the title field
    browser.find_element(By.ID, "title").send_keys("Markdown Test Post")

    # Interact with the EasyMDE editor
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("# Markdown Title\n\nThis is a **Markdown** post.").perform()

    # Submit the form
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Verify redirection to the posts list
    assert browser.current_url == f"{live_server_url}/admin/posts"
    assert "Post created successfully!" in browser.page_source  # Check for flash message

    # Verify the post is displayed correctly on the blog page
    browser.get(f"{live_server_url}/blog")
    assert "Markdown Test Post" in browser.page_source
    assert "<h1>Markdown Title</h1>" in browser.page_source
    assert "<p>This is a <strong>Markdown</strong> post.</p>" in browser.page_source

def test_create_post_with_empty_markdown(browser, live_server):
    """Test creating a post with an empty Markdown editor."""
    live_server_url = live_server.url()
    browser.get(f"{live_server_url}/admin/posts/new")

    # Fill out only the title field
    browser.find_element(By.ID, "title").send_keys("Empty Markdown Test")

    # Attempt to submit the form
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Check for the error message
    content_error = browser.find_element(By.ID, "content-error")
    assert content_error.is_displayed()
    assert content_error.text == "Content cannot be empty."

def test_edit_post(browser, live_server):
    """Test editing an existing post."""
    live_server_url = live_server.url()

    # Create a post programmatically
    browser.get(f"{live_server_url}/admin/posts/new")
    browser.find_element(By.ID, "title").send_keys("Test Post")
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("This is a test post.").perform()
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Navigate to the admin posts page
    browser.get(f"{live_server_url}/admin/posts")

    # Ensure there are posts in the list
    posts = browser.find_elements(By.LINK_TEXT, "Edit")
    assert len(posts) > 0, "No posts available to edit."

    # Click the edit button for the first post and get its ID
    post_element = posts[0]
    post_id = post_element.get_attribute("href").split("/")[-2]  # Extract the post ID from the URL
    post_element.click()

    # Assert that the browser navigates to the correct edit page
    assert browser.current_url == f"{live_server_url}/admin/posts/{post_id}/edit"

    # Update the form
    browser.find_element(By.ID, "title").clear()
    browser.find_element(By.ID, "title").send_keys("Updated Test Post")
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("This is an updated test post.").perform()
    
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    

    # Verify redirection to the posts list
    assert browser.current_url == f"{live_server_url}/admin/posts"
    assert "Post updated successfully!" in browser.page_source  # Check for flash message

def test_edit_post_with_markdown(browser, live_server):
    """Test editing a post with Markdown content."""
    live_server_url = live_server.url()

    # Create a post programmatically
    browser.get(f"{live_server_url}/admin/posts/new")
    browser.find_element(By.ID, "title").send_keys("Original Markdown Post")
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("# Original Title\n\nOriginal **content**.").perform()
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Navigate to the admin posts page and click edit
    browser.get(f"{live_server_url}/admin/posts")
    edit_button = browser.find_element(By.LINK_TEXT, "Edit")
    edit_button.click()

    # Update the Markdown content
    browser.find_element(By.ID, "title").clear()
    browser.find_element(By.ID, "title").send_keys("Updated Markdown Post")
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("\b" * 50 + "# Updated Title\n\nUpdated **content**.").perform()

    # Submit the form
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Verify the updated post is displayed correctly
    browser.get(f"{live_server_url}/blog")
    assert "Updated Markdown Post" in browser.page_source
    assert "<h1>Updated Title</h1>" in browser.page_source
    assert "<p>Updated <strong>content</strong>.</p>" in browser.page_source

def test_delete_post(browser, live_server):
    """Test deleting a post."""
    live_server_url = live_server.url()

    # Create a post programmatically
    browser.get(f"{live_server_url}/admin/posts/new")
    browser.find_element(By.ID, "title").send_keys("Test Post")
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("This is a test post.").perform()
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Navigate to the admin posts page
    browser.get(f"{live_server_url}/admin/posts")

    # Ensure there are posts in the list
    posts = browser.find_elements(By.CSS_SELECTOR, "form[action*='/delete']")
    assert len(posts) > 0, "No posts available to delete."

    # Locate the delete button for the first post
    delete_button = posts[0].find_element(By.CSS_SELECTOR, "button.btn-danger")

    # Click the delete button
    delete_button.click()

    # Wait for the alert to appear
    alert = WebDriverWait(browser, 2).until(EC.alert_is_present())

    # Confirm the deletion
    assert alert.text == "Are you sure you want to delete this post?"  # Check alert text
    alert.accept()

    # Verify redirection to the posts list
    assert browser.current_url == f"{live_server_url}/admin/posts"
    assert "Post deleted successfully!" in browser.page_source  # Check for flash message


def test_create_post_empty_title(browser, live_server):
    """Test form validation when creating a post with an empty title."""
    live_server_url = live_server.url()
    browser.get(f"{live_server_url}/admin/posts/new")

    # Fill out only the content field
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("This is a test post.").perform()

    # Attempt to submit the form
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Check for the error message
    title_error = browser.find_element(By.ID, "title-error")
    assert title_error.is_displayed()
    assert title_error.text == "Title cannot be empty."

def test_edit_post_empty_content(browser, live_server):
    """Test form validation when editing a post with empty content."""
    live_server_url = live_server.url()

    # Create a post programmatically
    browser.get(f"{live_server_url}/admin/posts/new")
    browser.find_element(By.ID, "title").send_keys("Test Post")
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("This is a test post.").perform()
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Navigate to the admin posts page and click edit
    browser.get(f"{live_server_url}/admin/posts")
    edit_button = browser.find_element(By.LINK_TEXT, "Edit")
    edit_button.click()

    # Clear the content field
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("\b" * 50).perform()

    # Attempt to submit the form
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Check for the error message
    content_error = browser.find_element(By.ID, "content-error")
    assert content_error.is_displayed()
    assert content_error.text == "Content cannot be empty."

