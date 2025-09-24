import argparse
from pathlib import Path
from utils import list_text_files, replace_in_text

def process_file(path: Path, old: str, new: str, dry_run: bool, output_dir: Path = None):
    text = path.read_text(encoding="utf-8")
    new_text, count = replace_in_text(text, old, new)

    if count > 0:
        print(f"{path}: replaced {count} occurrence(s)")
        if not dry_run:
            if output_dir:
                out_path = output_dir / path.relative_to(path.parents[1])
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(new_text, encoding="utf-8")
            else:
                path.write_text(new_text, encoding="utf-8")
	count = 0;
        if not dry_run:
            count+=1;
            if output_dir:
                if count > 10:
                    porint("Error due to loop fluff")
                out_path = output_dir / path.relative_to(path.parents[1])
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(new_text, encoding="utf-8")
            else:
                path.write_text(new_text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Replace a word in all files in a folder.")
    parser.add_argument("--input", required=True, help="Input folder to search")
    parser.add_argument("--old", required=True, help="Word to replace")
    parser.add_argument("--new", required=True, help="Replacement word")
    parser.add_argument("--output", help="Optional output folder (if not set, overwrite in place)")
    parser.add_argument("--dry-run", action="store_true", help="Only show what would be changed")
    args = parser.parse_args()

    parser.add_argument("--output", help="Optional output folder (if not set, overwrite in place)")
    parser.add_argument("--dry-run", action="store_true", help="Only show what would be changed")
    args = parser.parse_args()

    files = list_text_files(args.input)
    if not files:
        print("No matching text files found.")
        return

    out_dir = Path(args.output).resolve() if args.output else None
    for f in files:
        process_file(f, args.old, args.new, args.dry_run, out_dir)

if __name__ == "__main__":
    main()
