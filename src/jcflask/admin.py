from flask import Blueprint, render_template, request, redirect, url_for, flash
from jcflask.db import db
from jcflask.models import BlogPost

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/posts')
def list_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/list_posts.html', posts=posts)

@admin_bp.route('/posts/new', methods=['GET', 'POST'])
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

@admin_bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.session.get(BlogPost, post_id)  # Updated to session.get
    if not post:
        return redirect(url_for('admin.list_posts')), 404
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin.list_posts'))
    return render_template('admin/edit_post.html', post=post)

@admin_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = db.session.get(BlogPost, post_id)  # Updated to session.get
    if not post:
        return redirect(url_for('admin.list_posts')), 404
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin.list_posts'))
