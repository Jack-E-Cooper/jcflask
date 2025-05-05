from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('portfolio', __name__)

@bp.route('/portfolio')
def index():
    return render_template('portfolio.html', active_page='portfolio')