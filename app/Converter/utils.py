from pathlib import Path

def list_text_files(folder: str, exts=None):
    """List all text files in a folder with given extensions."""
    exts = exts or {".txt", ".md", ".py"}
    folder = Path(folder)
    return [p for p in folder.rglob("*") if p.suffix.lower() in exts]

def replace_in_text(content: str, old: str, new: str):
    """Replace all occurrences of old with new and return new text + count."""
    count = content.count(old)
    return content.replace(old, new), count
