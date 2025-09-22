from PyPDF2 import PdfReader
from pathlib import Path
import re

class PDFIndexer:
    def __init__(self):
        # inverted index: word -> list of {file, page, position}
        self.index = {}

    def add_occurrence(self, word, file, page, position):
        entry = {"file": str(file), "page": page+1, "position": position}
        self.index.setdefault(word.lower(), []).append(entry)

    def build_index(self, folder: Path):
        pdfs = list(folder.glob("*.pdf"))
        for pdf in pdfs:
            reader = PdfReader(str(pdf))
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                words = re.findall(r"\w+", text)
                for pos, word in enumerate(words):
                    self.add_occurrence(word, pdf.name, page_num, pos)

    def search(self, word):
        return self.index.get(word.lower(), [])
