from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('blog', __name__)

@bp.route('/blog')
def index():
    return render_template('blog.html', active_page='blog')