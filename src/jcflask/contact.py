from flask import Blueprint, render_template

bp = Blueprint("contact", __name__)


@bp.route("/contact", methods=["GET"])
def index():
    return render_template("contact.html", active_page="contact")
