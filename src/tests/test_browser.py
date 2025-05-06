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
    browser.find_element(By.ID, "title").send_keys("Test Post")

    # Interact with the EasyMDE editor
    editor_iframe = browser.find_element(By.CLASS_NAME, "CodeMirror")
    ActionChains(browser).move_to_element(editor_iframe).click().send_keys("This is a test post.").perform()

    # Submit the form
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


    # Verify redirection to the posts list
    assert browser.current_url == f"{live_server_url}/admin/posts"
    assert "Post created successfully!" in browser.page_source  # Check for flash message

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

def test_form_validation(browser, live_server):
    """Test form validation when creating a post."""
    live_server_url = live_server.url()
    browser.get(f"{live_server_url}/admin/posts/new")

    # Attempt to submit the form without filling it out
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    # Check for the browser's validation popup message
    title_field = browser.find_element(By.ID, "title")
    assert title_field.get_attribute("validationMessage") == "Please fill out this field."

    content_field = browser.find_element(By.ID, "content")
    assert content_field.get_attribute("validationMessage") == "Please fill out this field."
