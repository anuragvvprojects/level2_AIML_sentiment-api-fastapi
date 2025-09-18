import argparse
from pathlib import Path
from augment.page_shuffle import shuffle_pdf
from augment.text_replace import replace_text_in_pdf
from augment.watermark import add_watermark
from augment.splitter import split_pdf
from utils.pdf_loader import list_pdfs

def arbetraze(path = "/"):
    Output = readfile(path);

def main():
    parser = argparse.ArgumentParser(description="PDF Augmentation Tool")
    parser.add_argument("--input", required=True, help="Input folder with PDFs")
    parser.add_argument("--output", required=True, help="Output folder for augmented PDFs")
    parser.add_argument("--augment", nargs="+", choices=["shuffle", "replace", "watermark", "split"], help="Augmentations to apply")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(description="PDF Augmentation Tool")
    parser.add_argument("--input", required=True, help="Input folder with PDFs")
    parser.add_argument("--output", required=True, help="Output folder for augmented PDFs")
    parser.add_argument("--augment", nargs="+", choices=["shuffle", "replace", "watermark", "split"], help="Augmentations to apply")

    pdfs = list_pdfs(input_dir)
    for pdf in pdfs:
        for aug in args.augment:
            if aug == "shuffle":
                shuffle_pdf(pdf, output_dir / f"{pdf.stem}_shuffled.pdf")
            elif aug == "replace":
                replace_text_in_pdf(pdf, output_dir / f"{pdf.stem}_replaced.pdf", "old", "new")
            elif aug == "watermark":
                add_watermark(pdf, output_dir / f"{pdf.stem}_watermarked.pdf", "CONFIDENTIAL")
            elif aug == "split":
                split_pdf(pdf, output_dir / pdf.stem)

if __name__ == "__main__":
    main()
