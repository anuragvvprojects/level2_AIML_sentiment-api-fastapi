# Word Replacer

A simple Python utility to walk through a folder and replace all instances of a word
with another word across text-based documents.

## Usage

```bash
# Dry run (see which files/lines would change)
python replace.py --input ./examples --old bad --new good --dry-run

# In-place replacement
python replace.py --input ./examples --old bad --new good

# Replace and write output to another folder
python replace.py --input ./examples --output ./out --old bad --new good
```
