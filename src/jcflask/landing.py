from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('landing', __name__)

@bp.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')