from flask import Blueprint, render_template

bp = Blueprint("portfolio", __name__)

# Centralized project list for portfolio display
PROJECTS = [
    {
        "id": "flaskwebapp",
        "title": "Personal Website & Blog",
        "summary": "Developed a personal website and blog using Azure and Python Flask to showcase technical excellence in cloud security and DevSecOps. This project demonstrates end-to-end security practices such as CI/CD integration, secure code deployment, and the implementation of best practices in access control and monitoring.",
        "technologies": [
            "Azure",
            "Python",
            "Flask",
            "CI/CD",
            "DevSecOps",
            "Azure Key Vault",
        ],
        # "image": "/static/images/website_project.png"
    },
    {
        "id": "task_manager",
        "title": "Task Manager Web App",
        "summary": "A web application for managing tasks and to-dos. Built with Flask, SQLAlchemy, and Bootstrap. Features user authentication, CRUD operations, and a responsive UI.",
        "technologies": [
            "Flask",
            "SQLAlchemy",
            "Bootstrap",
            "User Authentication",
            "CRUD Operations",
            "Responsive Design",
        ],
        # "image": "/static/images/task_manager.png"
    },
    {
        "id": "blog_api",
        "title": "Blog RESTful API",
        "summary": "A RESTful API for a simple blog platform. Built with Flask-RESTful, JWT authentication, and Marshmallow for serialization.",
        "technologies": [
            "Flask-RESTful",
            "JWT Authentication",
            "Marshmallow",
            "API Development",
        ],
        # "image": "/static/images/blog_api.png"
    },
    {
        "id": "portfolio_website",
        "title": "Portfolio Website",
        "summary": "A portfolio website built with Flask and deployed on Heroku. Includes a contact form and project showcase.",
        "technologies": [
            "Flask",
            "Heroku",
            "Contact Form",
            "Project Showcase",
        ],
        # "image": "/static/images/portfolio_website.png"
    },
    {
        "id": "data_viz_dashboard",
        "title": "Data Visualization Dashboard",
        "summary": "A data visualization dashboard using Flask and Plotly Dash. Displays interactive charts and graphs from uploaded CSV files.",
        "technologies": [
            "Flask",
            "Plotly Dash",
            "Data Visualization",
            "CSV Files",
        ],
        # "image": "/static/images/data_viz_dashboard.png"
    },
    {
        "id": "static_site",
        "title": "Static Site with Flask-Frozen",
        "summary": "A static site generated with Flask-Frozen and deployed to Netlify.",
        "technologies": [
            "Flask-Frozen",
            "Netlify",
            "Static Site Generation",
        ],
        # "image": "/static/images/static_site.png"
    },
    # {
    #     "id": "physical_security",
    #     "title": "Physical Security & Policy Enhancements",
    #     "summary": "As an Information Systems Security Officer in the Canadian Armed Forces, spearheaded the update of physical security protocols in consultation with law enforcement agencies. Implemented comprehensive security audits and policy enhancements to respond to evolving threat intelligence.",
    #     "technologies": ["Security Audits", "Risk Assessment", "Policy Development", "Law Enforcement Collaboration"],
    #     "image": "/static/images/physical_security.png"
    # },
    # {
    #     "id": "crisis_management",
    #     "title": "Telecommunications & Crisis Management",
    #     "summary": "Led telecommunications operations and crisis response during the COVID-19 pandemic. Planned and executed disaster-resilient communications strategies for the Toronto Army Reserve. This initiative ensured effective remote work protocols and a rapid response to crisis situations.",
    #     "technologies": ["Telecommunications", "Crisis Management", "Remote Work Security", "IT Transition"],
    #     "image": "/static/images/crisis_management.png"
    # }
]


@bp.route("/portfolio")
def index():
    return render_template("portfolio.html", projects=PROJECTS, active_page="portfolio")
