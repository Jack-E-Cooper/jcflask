from flask import Blueprint, render_template, request, redirect, url_for, flash
from jcflask.db import db
from jcflask.models import BlogPost

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/posts')
def list_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/list_posts.html', posts=posts)

@bp.route('/posts/new', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = BlogPost(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success') 
        return redirect(url_for('admin.list_posts'))
    return render_template('admin/create_post.html')

@bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.session.get(BlogPost, post_id)
    if not post:
        flash('Post not found.', 'danger')
        return redirect(url_for('admin.list_posts'))
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin.list_posts'))
    return render_template('admin/edit_post.html', post=post)

@bp.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = db.session.get(BlogPost, post_id)
    if not post:
        flash('Post not found.', 'danger')
        return redirect(url_for('admin.list_posts'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin.list_posts'))
