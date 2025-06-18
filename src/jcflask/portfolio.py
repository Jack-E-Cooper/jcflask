from flask import Blueprint, render_template, current_app
from .project import PROJECTS
from flask import url_for

bp = Blueprint("portfolio", __name__)

def get_portfolio_projects():
    """Return a list of project summaries for the portfolio page, with correct image URLs using image_url helper."""
    image_url = current_app.jinja_env.globals["image_url"]
    projects = []
    for pid, pdata in PROJECTS.items():
        projects.append({
            "id": pid,
            "title": pdata["title"],
            "summary": pdata.get("summary") or pdata.get("description", ""),
            "technologies": pdata.get("technologies", []),
            "image": image_url(pdata.get("image")),
        })
    return projects

@bp.route("/portfolio")
def index():
    return render_template("portfolio.html", projects=get_portfolio_projects(), active_page="portfolio")
