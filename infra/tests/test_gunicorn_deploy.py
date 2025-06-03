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
