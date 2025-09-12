from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path

def split_pdf(input_path, output_folder):
    reader = PdfReader(str(input_path))
    output_folder.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        out_file = output_folder / f"page_{i+1}.pdf"
        with open(out_file, "wb") as f:
            writer.write(f)
