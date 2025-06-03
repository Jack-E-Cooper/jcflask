import subprocess
import glob
import os


def test_bicep_files_are_valid():
    bicep_files = glob.glob(
        os.path.join(os.path.dirname(__file__), "..", "*.bicep"), recursive=True
    )
    for bicep_file in bicep_files:
        result = subprocess.run(
            ["az", "bicep", "build", "--file", bicep_file],
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode == 0
        ), f"Bicep syntax error in {bicep_file}:\n{result.stderr}"
