import re

def extract_diff(text):
    match = re.search(r"```diff(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None

def apply_patch(original, diff):
    new_lines = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            new_lines.append(line[1:])
        elif line.startswith("-"):
            continue
        elif not line.startswith("@") and not line.startswith("---"):
            new_lines.append(line)
    return "\n".join(new_lines)
