from flask import Blueprint, render_template
from werkzeug.exceptions import abort
from jcflask.db import db
from jcflask.models import BlogPost
import markdown  # Add this import

bp = Blueprint("blog", __name__)


@bp.route("/blog")
def index():
    """Display a list of blog posts."""
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template("blog.html", active_page="blog", posts=posts)


@bp.route("/blog/<int:post_id>")
def view_post(post_id):
    """Display a single blog post."""
    post = db.session.get(
        BlogPost, post_id
    )  # Use Session.get() for SQLAlchemy 2.0 compatibility
    if not post:
        abort(404)
    post.content = markdown.markdown(post.content)  # Render Markdown to HTML
    return render_template("view_post.html", active_page="blog", post=post)
