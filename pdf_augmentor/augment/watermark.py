from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def create_watermark(text):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 40)
    can.setFillGray(0.5, 0.5)
    can.drawCentredString(300, 400, text)
    can.save()
    packet.seek(0)
    return PdfReader(packet)

def add_watermark(input_path, output_path, text):
    watermark = create_watermark(text)
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(watermark.pages[0])
        writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
