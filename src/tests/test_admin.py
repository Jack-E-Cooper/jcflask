from jcflask.models import BlogPost
from jcflask.db import db
import markdown

def test_admin_create_post(client, app):
    response = client.post('/admin/posts/new', data={
        'title': 'Test Post',
        'content': 'This is a test post.'
    })
    assert response.status_code == 302  # Redirect after creation

    with app.app_context():
        post = BlogPost.query.filter_by(title='Test Post').first()
        assert post is not None
        assert post.content == 'This is a test post.'

def test_admin_edit_post(client, app):
    with app.app_context():
        post = BlogPost(title='Old Title', content='Old Content')
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    response = client.post(f'/admin/posts/{post_id}/edit', data={
        'title': 'New Title',
        'content': 'New Content'
    })
    assert response.status_code == 302  # Redirect after edit

    with app.app_context():
        post = db.session.get(BlogPost, post_id)  # Updated to session.get
        assert post.title == 'New Title'
        assert post.content == 'New Content'

def test_admin_delete_post(client, app):
    with app.app_context():
        post = BlogPost(title='Delete Me', content='To be deleted')
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    response = client.post(f'/admin/posts/{post_id}/delete')
    assert response.status_code == 302  # Redirect after deletion

    with app.app_context():
        post = db.session.get(BlogPost, post_id)  # Updated to session.get
        assert post is None

def test_admin_create_markdown_post(client, app):
    markdown_content = "# Markdown Title\n\nThis is a **Markdown** post."
    response = client.post('/admin/posts/new', data={
        'title': 'Markdown Test Post',
        'content': markdown_content
    })
    assert response.status_code == 302  # Redirect after creation

    with app.app_context():
        post = BlogPost.query.filter_by(title='Markdown Test Post').first()
        assert post is not None
        assert post.content == markdown_content

def test_view_markdown_post(client, app):
    markdown_content = "# Markdown Title\n\nThis is a **Markdown** post."
    with app.app_context():
        post = BlogPost(title="Markdown Test Post", content=markdown_content)
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    response = client.get(f'/blog/{post_id}')
    assert response.status_code == 200
    assert b"<h1>Markdown Title</h1>" in response.data  # Check rendered Markdown
    assert b"<p>This is a <strong>Markdown</strong> post.</p>" in response.data
