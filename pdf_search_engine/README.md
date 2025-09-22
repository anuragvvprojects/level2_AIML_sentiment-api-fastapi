# PDF Search Engine

This project indexes a folder of PDF files into an inverted index that maps words -> occurrences (file, page, location).
You can then search for a word and retrieve all occurrences.

## Features
- Extract text from PDFs using PyPDF2
- Build an inverted index (dictionary: word -> list of (file, page, position))
- Search efficiently for any word
- Example usage included

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py --input ./examples --search intelligence
```
