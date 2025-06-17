from flask import Blueprint, render_template
from .project import get_portfolio_projects  # Import the helper

bp = Blueprint("portfolio", __name__)

@bp.route("/portfolio")
def index():
    return render_template("portfolio.html", projects=get_portfolio_projects(), active_page="portfolio")
