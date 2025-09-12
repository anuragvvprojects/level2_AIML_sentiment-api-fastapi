from pathlib import Path

def list_pdfs(folder: Path):
    return [p for p in folder.glob("*.pdf")]
