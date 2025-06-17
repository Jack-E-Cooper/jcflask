import pytest
from jcflask.db import db
from jcflask.models import BlogPost

pytestmark = pytest.mark.skipif(
    not hasattr(pytest, "flask_app") or not getattr(pytest.flask_app.config, "ENABLE_BLOG", False),
    reason="Blog feature is disabled (ENABLE_BLOG is False)"
)


def test_blog_post_model(app):
    with app.app_context():
        # Create a new blog post
        post = BlogPost(title="Test Post", content="This is a test post.")
        db.session.add(post)
        db.session.commit()

        # Query the blog post
        retrieved_post = BlogPost.query.first()
        assert retrieved_post is not None
        assert retrieved_post.title == "Test Post"
        assert retrieved_post.content == "This is a test post."

        # Clean up
        db.session.delete(retrieved_post)
        db.session.commit()


def test_blog_index(client, app):
    with app.app_context():
        # Create test blog posts
        post1 = BlogPost(title="Post 1", content="Content for post 1")
        post2 = BlogPost(title="Post 2", content="Content for post 2")
        db.session.add_all([post1, post2])
        db.session.commit()

    # Test blog index
    response = client.get("/blog")
    assert response.status_code == 200
    assert b"Post 1" in response.data
    assert b"Post 2" in response.data


def test_view_post(client, app):
    with app.app_context():
        # Create a test blog post
        post = BlogPost(title="Test Post", content="This is a test post.")
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    # Test viewing the individual post
    response = client.get(f"/blog/{post_id}")
    assert response.status_code == 200
    assert b"Test Post" in response.data
    assert b"This is a test post." in response.data
