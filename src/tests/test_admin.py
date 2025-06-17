from jcflask.models import BlogPost
from jcflask.db import db
import pytest


@pytest.fixture(autouse=True)
def reset_database(app):
    """Reset the database before each test."""
    with app.app_context():
        db.session.query(BlogPost).delete()
        db.session.commit()


def test_admin_create_post(client, app):
    if not app.config.get("ENABLE_BLOG", False):
        pytest.skip("Blog feature is disabled (ENABLE_BLOG is False)")
    """Test creating a new post."""
    response = client.post(
        "/admin/posts/new",
        data={"title": "Test Post", "content": "This is a test post."},
    )
    assert response.status_code == 302

    with app.app_context():
        post = BlogPost.query.filter_by(title="Test Post").first()
        assert post is not None
        assert post.content == "This is a test post."


def test_admin_edit_post(client, app):
    if not app.config.get("ENABLE_BLOG", False):
        pytest.skip("Blog feature is disabled (ENABLE_BLOG is False)")
    with app.app_context():
        post = BlogPost(title="Old Title", content="Old Content")
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    response = client.post(
        f"/admin/posts/{post_id}/edit",
        data={"title": "New Title", "content": "New Content"},
    )
    assert response.status_code == 302

    with app.app_context():
        post = db.session.get(BlogPost, post_id)
        assert post.title == "New Title"
        assert post.content == "New Content"


def test_admin_delete_post(client, app):
    if not app.config.get("ENABLE_BLOG", False):
        pytest.skip("Blog feature is disabled (ENABLE_BLOG is False)")
    with app.app_context():
        post = BlogPost(title="Delete Me", content="To be deleted")
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    response = client.post(f"/admin/posts/{post_id}/delete")
    assert response.status_code == 302

    with app.app_context():
        post = db.session.get(BlogPost, post_id)
        assert post is None


def test_admin_create_markdown_post(client, app):
    if not app.config.get("ENABLE_BLOG", False):
        pytest.skip("Blog feature is disabled (ENABLE_BLOG is False)")
    markdown_content = "# Markdown Title\n\nThis is a **Markdown** post."
    response = client.post(
        "/admin/posts/new",
        data={"title": "Markdown Test Post", "content": markdown_content},
    )
    assert response.status_code == 302

    with app.app_context():
        post = BlogPost.query.filter_by(title="Markdown Test Post").first()
        assert post is not None
        assert post.content == markdown_content


def test_view_markdown_post(client, app):
    if not app.config.get("ENABLE_BLOG", False):
        pytest.skip("Blog feature is disabled (ENABLE_BLOG is False)")
    markdown_content = "# Markdown Title\n\nThis is a **Markdown** post."
    with app.app_context():
        post = BlogPost(title="Markdown Test Post", content=markdown_content)
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    response = client.get(f"/blog/{post_id}")
    assert response.status_code == 200
    assert b"<h1>Markdown Title</h1>" in response.data
    assert b"<p>This is a <strong>Markdown</strong> post.</p>" in response.data


def test_database_starts_empty(client, app):
    if not app.config.get("ENABLE_BLOG", False):
        pytest.skip("Blog feature is disabled (ENABLE_BLOG is False)")
    """Test that the database starts empty."""
    with app.app_context():
        posts = BlogPost.query.all()
        assert len(posts) == 0, "Database should start empty."
