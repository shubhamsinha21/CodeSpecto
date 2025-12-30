import re

def parse_code(file_obj):
    content = file_obj["content"]
    language = file_obj["language"]

    imports, symbols = [], []

    if language == "python":
        imports = re.findall(r"(?:import|from)\s+(\w+)", content)
        symbols = re.findall(r"(?:def|class)\s+(\w+)", content)

    file_obj["imports"] = list(set(imports))
    file_obj["symbols"] = list(set(symbols))
    return file_obj
