import os
import re
import glob
import subprocess
import sys
import time


def test_linux_fx_version_for_gunicorn():
    bicep_files = glob.glob(
        os.path.join(os.path.dirname(__file__), "..", "*.bicep"), recursive=True
    )
    found = False
    for filepath in bicep_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            # Look for linuxFxVersion set to Python
            if re.search(r"linuxFxVersion\s*:\s*'PYTHON\|3\.11'", content):
                found = True
    assert (
        found
    ), "No Bicep file configures linuxFxVersion for Python 3.11, required for Gunicorn deployment."


def test_gunicorn_entrypoint_exists_and_is_correct():
    """
    Ensure the Gunicorn entrypoint file and app object exist and are correct.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    main_py = os.path.join(project_root, "main.py")
    assert os.path.exists(main_py), (
        "main.py not found at project root. "
        "Gunicorn startup command 'gunicorn main:app' will fail."
    )

    # Check that 'app' is defined in main.py
    with open(main_py, "r", encoding="utf-8") as f:
        content = f.read()
        assert "app = create_app()" in content or "app=create_app()" in content.replace(
            " ", ""
        ), (
            "'app = create_app()' not found in main.py. "
            "Gunicorn requires 'app' to be defined for 'gunicorn main:app'."
        )


def test_gunicorn_can_start_app():
    """
    Test that Gunicorn can start the Flask app using the expected entrypoint.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    main_py = os.path.join(project_root, "main.py")
    app_module = "main:app"
    if not os.path.exists(main_py):
        # Skip if main.py does not exist in the expected location
        return

    try:
        proc = subprocess.Popen(
            [sys.executable, "-m", "gunicorn", app_module, "--bind", "127.0.0.1:5005"],
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(3)  # Give gunicorn time to start
        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            raise AssertionError(
                f"Gunicorn failed to start the app. Return code: {proc.returncode}\n"
                f"STDOUT:\n{stdout.decode()}\nSTDERR:\n{stderr.decode()}"
            )
    finally:
        if "proc" in locals() and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)


def test_azure_appservice_python_env():
    """
    Ensure the Python version matches Azure App Service expectations (3.11.x).
    """
    import sys

    python_version = sys.version_info
    print("Python version:", sys.version)
    assert python_version.major == 3 and python_version.minor == 11, (
        f"Python version is {python_version.major}.{python_version.minor}, "
        "but Azure App Service is configured for Python 3.11"
    )


def test_requirements_installed_for_azure_webapp():
    """
    Ensure all modules in requirements.txt are importable, as Azure Web Apps expects after deployment.
    Also output diagnostics to verify the Python environment in use.
    """
    import importlib
    import sys
    import os

    # Mapping from PyPI package names to import names
    MODULE_IMPORT_SUBSTITUTIONS = {
        "beautifulsoup4": "bs4",
        "pillow": "PIL",
        "pyyaml": "yaml",
        "scikit-learn": "sklearn",
        "opencv-python": "cv2",
        "python-dotenv": "dotenv",
        "flask-restful": "flask_restful",
        "flask-sqlalchemy": "flask_sqlalchemy",
        "flask-login": "flask_login",
        "flask-migrate": "flask_migrate",
        "flask-wtf": "flask_wtf",
        "flask-cors": "flask_cors",
        "flask-mail": "flask_mail",
        "flask-marshmallow": "flask_marshmallow",
        "azure-identity": "azure.identity",
        "azure_identity": "azure.identity",
        "azure_keyvault_secrets": "azure.keyvault.secrets",
        "azure-mgmt-resource": "azure.mgmt.resource",
        "azure-mgmt-web": "azure.mgmt.web",
        "azure-storage-blob": "azure.storage.blob",
        "azure-storage-queue": "azure.storage.queue",
        "azure-storage-file-share": "azure.storage.fileshare",
        "azure-common": "azure.common",
        "azure-core": "azure.core",
        "msal": "msal",
        "requests": "requests",
        "marshmallow": "marshmallow",
        "gunicorn": "gunicorn",
        "pytest": "pytest",
        "sqlalchemy": "sqlalchemy",
        "setuptools": "setuptools",
        "wheel": "wheel",
        # Add more as needed
    }

    print("Python executable:", sys.executable)
    print("sys.path:", sys.path)
    print("PYTHONPATH:", os.environ.get("PYTHONPATH", ""))
    print("VIRTUAL_ENV:", os.environ.get("VIRTUAL_ENV", ""))
    try:
        import site
        print("site.getsitepackages():", getattr(site, "getsitepackages", lambda: "N/A")())
    except Exception as e:
        print("Could not get site-packages:", e)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    requirements_path = os.path.join(project_root, "requirements.txt")
    assert os.path.exists(requirements_path), "requirements.txt not found at project root."

    with open(requirements_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Extract the module name (handles 'package==version' and similar)
            module = line.split("==")[0].split(">=")[0].split("<=")[0].split("[")[0].replace("-", "_").strip()
            if not module:
                continue
            import_names = [module]
            # Add lowercase version if different
            if module.lower() != module:
                import_names.append(module.lower())
            # Add substitution if present
            if module.lower() in MODULE_IMPORT_SUBSTITUTIONS:
                import_names.append(MODULE_IMPORT_SUBSTITUTIONS[module.lower()])
            # Try all possible import names
            for import_name in import_names:
                try:
                    importlib.import_module(import_name)
                    break
                except ImportError:
                    continue
            else:
                raise AssertionError(f"Module '{module}' from requirements.txt could not be imported using any of: {import_names}")
