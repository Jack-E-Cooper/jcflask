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
    Ensure the environment variables and PATH are set as Azure App Service expects for Python.
    """
    # Simulate the Azure App Service Linux environment
    python_path = os.environ.get("PYTHONPATH", "")
    path = os.environ.get("PATH", "")
    python_home = os.environ.get("PYTHONHOME", "")
    python_exe = sys.executable

    # Azure App Service for Linux typically uses /usr/local/bin/python3.11 or /usr/bin/python3.11
    assert "python" in python_exe, "Python executable not found in expected location"
    assert any(
        p in python_exe for p in ["/usr/local/bin/python3.11", "/usr/bin/python3.11", "/opt/python/3.11.*/bin/python3.11"]
    ), f"Python executable path '{python_exe}' is not typical for Azure App Service for Linux Python 3.11"

    # PATH should include the directory of the python executable
    python_dir = os.path.dirname(python_exe)
    assert python_dir in path.split(":"), f"Python directory '{python_dir}' not found in PATH"

    # PYTHONHOME is usually unset or set to the python installation root
    if python_home:
        assert python_home in python_exe, "PYTHONHOME does not match Python executable location"


def test_requirements_installed_for_azure_webapp():
    """
    Ensure all modules in requirements.txt are importable, as Azure Web Apps expects after deployment.
    """
    import importlib

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
            # Some packages have different import names; skip known problematic ones or handle mapping if needed
            try:
                importlib.import_module(module)
            except ImportError as e:
                raise AssertionError(f"Module '{module}' from requirements.txt could not be imported: {e}")
