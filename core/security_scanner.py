import re

SECRET_PATTERNS = [
    r"api[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
    r"secret\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
    r"token\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
]

DANGEROUS_FUNCTIONS = ["eval(", "exec("]

SQL_PATTERNS = [
    r"SELECT .* FROM .* WHERE .* = .*\\+",
    r"execute\\(.*\\+.*\\)"
]

def scan_file(file_obj):
    issues = []
    content = file_obj["content"]
    path = file_obj["file_path"]

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append({
                "file": path,
                "issue": "Hardcoded secret detected",
                "severity": "HIGH"
            })

    for fn in DANGEROUS_FUNCTIONS:
        if fn in content:
            issues.append({
                "file": path,
                "issue": f"Dangerous function usage: {fn}",
                "severity": "HIGH"
            })

    for pattern in SQL_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append({
                "file": path,
                "issue": "Possible SQL injection risk",
                "severity": "MEDIUM"
            })

    return issues

def scan_files(file_index):
    results = []
    for f in file_index:
        results.extend(scan_file(f))
    return results
