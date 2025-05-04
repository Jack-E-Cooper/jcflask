from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('about', __name__)

@bp.route('/about')
def index():
    return render_template('about.html')