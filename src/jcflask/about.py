from flask import Blueprint, render_template

bp = Blueprint("about", __name__)


@bp.route("/about")
def index():
    return render_template("about.html", active_page="about")
