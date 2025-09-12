import random
from PyPDF2 import PdfReader, PdfWriter

def shuffle_pdf(input_path, output_path):
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    pages = list(range(len(reader.pages)))
    random.shuffle(pages)
    for i in pages:
        writer.add_page(reader.pages[i])
    with open(output_path, "wb") as f:
        writer.write(f)
