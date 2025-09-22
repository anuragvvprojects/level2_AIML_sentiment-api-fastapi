import argparse
from pathlib import Path
from pdfsearch.indexer import PDFIndexer

def main():
    parser = argparse.ArgumentParser(description="Search PDFs for words.")
    parser.add_argument("--input", required=True, help="Folder with PDFs")
    parser.add_argument("--search", required=True, help="Word to search for")
    args = parser.parse_args()

    folder = Path(args.input)
    indexer = PDFIndexer()
    indexer.build_index(folder)

    results = indexer.search(args.search)
    if not results:
        print(f"No occurrences of '{args.search}' found.")
    else:
        for r in results:
            print(f"File: {r['file']} | Page: {r['page']} | Position: {r['position']}")

if __name__ == "__main__":
    main()
