from flask import (
    Blueprint, render_template, abort
)
from werkzeug.exceptions import NotFound

bp = Blueprint('project', __name__, url_prefix='/project')

# Mock data for demonstration purposes
PROJECTS = {
    "project1": {
        "title": "Project 1",
        "description": "This is a detailed description of Project 1.",
        "technologies": ["Python", "Flask", "Azure"],
        "github_link": "https://github.com/johncooper/project1",
        "demo_link": "https://project1-demo.com",
        "updated_at": "2023-10-01"
    },
    "project2": {
        "title": "Project 2",
        "description": "This is a detailed description of Project 2.",
        "technologies": ["JavaScript", "React", "Node.js"],
        "github_link": "https://github.com/johncooper/project2",
        "demo_link": None,
        "updated_at": "2023-09-15"
    }
}

@bp.route('/<project_id>')
def view_project(project_id):
    project = PROJECTS.get(project_id)
    if not project:
        raise NotFound(f"Project with ID '{project_id}' not found.")
    return render_template('project.html', project=project)
