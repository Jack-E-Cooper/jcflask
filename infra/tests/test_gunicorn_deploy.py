import os
import re
import glob
import subprocess
import sys
import time

def test_linux_fx_version_for_gunicorn():
    bicep_files = glob.glob(os.path.join(os.path.dirname(__file__), '..', '*.bicep'), recursive=True)
    found = False
    for filepath in bicep_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for linuxFxVersion set to Python
            if re.search(r"linuxFxVersion\s*:\s*'PYTHON\|3\.11'", content):
                found = True
    assert found, "No Bicep file configures linuxFxVersion for Python 3.11, required for Gunicorn deployment."

def test_gunicorn_can_start_app():
    """
    Test that Gunicorn can start the Flask app using the expected entrypoint.
    """
    app_module = "app:jcflask"  # Change if your app entrypoint is different
    app_py = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app.py'))
    if not os.path.exists(app_py):
        # Skip if app.py does not exist in the expected location
        return

    # Try to start gunicorn with the app module
    try:
        proc = subprocess.Popen(
            [sys.executable, '-m', 'gunicorn', app_module, '--bind', '127.0.0.1:5005'],
            cwd=os.path.dirname(app_py),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)  # Give gunicorn time to start
        assert proc.poll() is None, "Gunicorn failed to start the app."
    finally:
        if 'proc' in locals() and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
