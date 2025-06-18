from flask import Blueprint, render_template, url_for, current_app
from werkzeug.exceptions import NotFound

bp = Blueprint("project", __name__, url_prefix="/project")

# Centralized project data
PROJECTS = {
    "flaskwebapp": {
        "title": "Personal Website & Blog",
        "summary": "Developed a personal website and blog using Azure and Python Flask to showcase technical excellence in cloud security and DevSecOps.",
        "description": "This project is a personal website and blog built with Python Flask and deployed on Azure. It demonstrates secure web development, CI/CD automation, and DevSecOps best practices. The site features a portfolio, blog, and contact form, all designed with a focus on all-hazards security and organizational resilience.",
        "technologies": [
            "Python",
            "Flask",
            "Azure",
            "CI/CD",
            "DevSecOps",
            "Azure Key Vault",
        ],
        "github_link": "https://github.com/Jack-E-Cooper/jcflask",
        # "demo_link": "/",
        "updated_at": "2025-06-02",
        "image": "jc_portfolio_project_image.png",  # Just the filename for local use
        "prod_image_url": "https://jcflaskfilestore.blob.core.windows.net/jcflask-website-images/jc_portfolio_project_image.png",
        "embed_html": """
        <!-- Example embedded element -->
        <iframe src="https://example.com/demo" width="100%" height="300" frameborder="0"></iframe>
        """,
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
        """,
    },
    "toastmasters_fee_analysis": {
        "title": "Toastmasters Club Fee What-If Analysis",
        "summary": "Interactive Office 365 Excel sheet for exploring different member fee schedules for our Toastmasters club.",
        "description": "This project uses an embedded Office 365 Excel workbook to allow club officers and members to perform what-if analysis on membership fee schedules. Users can adjust variables and immediately see the impact on club finances, helping with transparent and data-driven decision making.",
        "technologies": [
            "Microsoft Excel",
            "Excel Online",
            "Embed",
        ],
        "github_link": "",
        "updated_at": "2025-06-02",
        "image": "TMExcelWhatIf.png", 
        "prod_image_url": "https://jcflaskfilestore.blob.core.windows.net/jcflask-website-images/TMExcelWhatIf.png",
        "embed_html": """
        <iframe width="700" height="900" frameborder="0" scrolling="yes" src="https://1drv.ms/x/c/2b30a3c5a46267c0/IQRMBZDjPc-NQJ-FzWUddAR0AdfwXqddAgI7fHV-iUReTG4?em=2&wdAllowInteractivity=False&AllowTyping=True&wdHideGridlines=True&wdHideHeaders=True&wdInConfigurator=True&wdInConfigurator=True"></iframe>
        """,
        "writeup": """
        <h3>What-If Analysis for Toastmasters Club Fees</h3>
        <p>
        This project provides an interactive Excel workbook embedded directly in the website, enabling club members and officers to experiment with different fee structures and instantly see the financial impact. It's a practical tool for transparent, collaborative budgeting and planning.
        </p>
        <ul>
          <li>Adjust membership fee variables and see real-time results</li>
          <li>Facilitates open discussion and data-driven decisions</li>
          <li>Accessible from any device via the web</li>
        </ul>
        """,
    },
    "toastmasters": {
        "title": "Toastmasters International: Innovative Planning & Leadership",
        "summary": "Achievements in Toastmasters: Level 3 Innovative Planning, contest finalist, club leadership, and mentorship.",
        "description": (
            "As an active member of Toastmasters International, I am currently finishing Level 3 in the Innovative Planning Pathway. "
            "In 2025, I placed 3rd at the Division Contest for English Improvisational Speaking in Nice, France. "
            "I served as Vice President Membership (VPM) on the Executive Committee (EXCOM) for 2025, growing club membership from 14 to 22. "
            "Throughout my journey, I have both mentored new members and benefited from the mentorship of experienced Toastmasters."
        ),
        "technologies": [
            "Public Speaking",
            "Leadership",
            "Mentorship",
            "Innovative Planning",
            "Event Organization",
            "Toastmasters Pathways"
        ],
        "github_link": "",
        "updated_at": "2025-06-02",
        "image": "DTKT_speak_lead_grow.png",
        "prod_image_url": "https://jcflaskfilestore.blob.core.windows.net/jcflask-website-images/DTKT_speak_lead_grow.png",
        "embed_html": """
        <video class="img-fluid rounded shadow-sm" style="background:#000; width:100%; max-width:700px;" controls poster="/static/images/DTKT_speak_lead_grow.png">
          <source src="/static/videos/RES_presentation_video.mp4" type="video/mp4; codecs='avc1.42E01E, mp4a.40.2'">
          Your browser does not support the video tag.
        </video>
        """,
        "writeup": """
        <h3>Toastmasters Achievements</h3>
        <ul>
          <li>Finishing Level 3 in the <strong>Innovative Planning</strong> Pathway</li>
          <li><strong>3rd Place</strong> at the Division Contest for English Improvisational Speaking (Nice, 2025)</li>
          <li>Served as <strong>VP Membership</strong> (EXCOM, 2025): grew club from 14 to 22 members</li>
          <li>Mentored new members and received mentorship from experienced Toastmasters</li>
        </ul>
        <p>
        The video below is from a club presentation, demonstrating my growth in public speaking and leadership.
        </p>
        """,
    },
    # ...add more projects as needed...
}

def get_portfolio_projects():
    """Return a list of project summaries for the portfolio page, with correct image URLs."""
    app = current_app._get_current_object()
    is_debug = getattr(app, "debug", False)
    env = current_app.config.get("ENV", "production")
    projects = []
    for pid, pdata in PROJECTS.items():
        # Use static image if in debug mode or not production
        if is_debug or env != "production":
            image_url = url_for("static", filename=f"images/{pdata.get('image')}")
        else:
            image_url = pdata.get("prod_image_url")
        projects.append({
            "id": pid,
            "title": pdata["title"],
            "summary": pdata.get("summary") or pdata.get("description", ""),
            "technologies": pdata.get("technologies", []),
            "image": image_url,
        })
    return projects

@bp.route("/<project_id>", endpoint="view_project")
def view_project(project_id):
    project = PROJECTS.get(project_id)
    if not project:
        raise NotFound(f"Project with ID '{project_id}' not found.")
    app = current_app._get_current_object()
    is_debug = getattr(app, "debug", False)
    env = current_app.config.get("ENV", "production")
    print(f"[DEBUG] view_project: ENV={env}, debug={is_debug}")
    # Use static image if in debug mode or not production
    if is_debug or env != "production":
        project["display_image"] = url_for("static", filename=f"images/{project.get('image')}")
    else:
        project["display_image"] = project.get("prod_image_url")
    return render_template("project.html", project=project)
