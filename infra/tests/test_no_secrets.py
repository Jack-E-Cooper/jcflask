import os
import re
import glob

SECRET_PATTERNS = [
    re.compile(r'password\s*=\s*["\'].*["\']', re.IGNORECASE),
    re.compile(r'client_secret\s*=\s*["\'].*["\']', re.IGNORECASE),
    re.compile(r'key\s*=\s*["\'].*["\']', re.IGNORECASE),
    re.compile(r'connectionstring\s*=\s*["\'].*["\']', re.IGNORECASE),
    re.compile(r'(?i)secret', re.IGNORECASE),
]

def test_infra_files_do_not_contain_secrets():
    infra_files = glob.glob(os.path.join(os.path.dirname(__file__), '..', '*.bicep'), recursive=True)
    for filepath in infra_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for pattern in SECRET_PATTERNS:
                assert not pattern.search(content), f"Potential secret found in {filepath}: {pattern.pattern}"
