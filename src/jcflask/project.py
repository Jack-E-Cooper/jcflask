from flask import (
    Blueprint, render_template
)
from werkzeug.exceptions import NotFound

bp = Blueprint('project', __name__, url_prefix='/project')

# Centralized project data
PROJECTS = {
    "flaskwebapp": {
        "title": "Personal Website & Blog",
        "description": "This project is a personal website and blog built with Python Flask and deployed on Azure. It demonstrates secure web development, CI/CD automation, and DevSecOps best practices. The site features a portfolio, blog, and contact form, all designed with a focus on all-hazards security and organizational resilience.",
        "technologies": ["Python", "Flask", "Azure", "CI/CD", "DevSecOps", "Azure Key Vault"],
        "github_link": "https://github.com/Jack-E-Cooper/jcflask",
        # "demo_link": "/",
        "updated_at": "2025-06-02",
        "writeup": """
        <h3>Project Overview</h3>
        <p>
        This webapp is a showcase of secure, scalable web application development using Python Flask and Azure. It incorporates best practices in cloud deployment, automated pipelines, and security controls, with a focus on all-hazards security principles.
        </p>
        <h4>Key Features</h4>
        <ul>
          <li>Azure-based deployment with automated CI/CD pipelines</li>
          <li>Role-based access control and secure secrets management</li>
          <li>Comprehensive logging and monitoring</li>
          <li>Documentation of security controls and risk management processes</li>
        </ul>
        <h4>Impact</h4>
        <p>
        This project serves as a template for resilient, secure web services, integrating information security, policy, and operational continuity for organizations seeking robust digital solutions.
        </p>
        """
    },
    # "physical_security": {
    #     "title": "Physical Security & Policy Enhancements",
    #     "description": "As an Information Systems Security Officer in the Canadian Armed Forces, spearheaded the update of physical security protocols in consultation with law enforcement agencies. Implemented comprehensive security audits and policy enhancements to respond to evolving threat intelligence.",
    #     "technologies": ["Security Audits", "Risk Assessment", "Policy Development", "Law Enforcement Collaboration"],
    #     "github_link": "",
    #     "demo_link": "",
    #     "updated_at": "2023-09-01",
    #     "writeup": ""
    # },
    # "crisis_management": {
    #     "title": "Telecommunications & Crisis Management",
    #     "description": "Led telecommunications operations and crisis response during the COVID-19 pandemic. Planned and executed disaster-resilient communications strategies for the Toronto Army Reserve. This initiative ensured effective remote work protocols and a rapid response to crisis situations.",
    #     "technologies": ["Telecommunications", "Crisis Management", "Remote Work Security", "IT Transition"],
    #     "github_link": "",
    #     "demo_link": "",
    #     "updated_at": "2023-08-01",
    #     "writeup": ""
    # }
}

@bp.route('/<project_id>', endpoint='view_project')
def view_project(project_id):
    project = PROJECTS.get(project_id)
    if not project:
        raise NotFound(f"Project with ID '{project_id}' not found.")
    return render_template('project.html', project=project)
