import os

EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "javascript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".cpp": "cpp",
    ".c": "c",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".md": "markdown",
}

def detect_language(filename):
    return EXTENSION_LANGUAGE_MAP.get(
        os.path.splitext(filename)[1].lower(),
        "text"
    )

def build_file_index(files: dict):
    index = []
    for path, content in files.items():
        index.append({
            "file_path": path,
            "language": detect_language(path),
            "size": len(content),
            "content": content
        })
    return index
