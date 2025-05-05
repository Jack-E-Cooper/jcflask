from jcflask.db import db
from jcflask.models import BlogPost

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
