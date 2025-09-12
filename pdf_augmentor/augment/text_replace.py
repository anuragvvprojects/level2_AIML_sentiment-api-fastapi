from PyPDF2 import PdfReader, PdfWriter

def replace_text_in_pdf(input_path, output_path, old_word, new_word):
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text = text.replace(old_word, new_word)
            # NOTE: PyPDF2 cannot rewrite text directly, so this is just a stub
        writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
