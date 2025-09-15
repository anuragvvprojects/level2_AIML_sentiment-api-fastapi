import json
import pandas as pd
import os

JSON_PATH = "data/raw/CUAD_v1/CUAD_v1.json"
CSV_PATH = "data/raw/CUAD_v1/master_clauses.csv"
TXT_DIR = "data/raw/CUAD_v1/full_contract_txt/"

def inspect_json(path):
    with open(path, "r") as f:
        data = json.load(f)

    if isinstance(data, dict):
        print("✅ JSON is a dict")
        print("Top-level keys:", list(data.keys())[:5])
        sample_key = list(data.keys())[0]
        sample_doc = data[sample_key]
        print(f"\n📄 Sample document: {sample_key}")
        print("Keys:", list(sample_doc.keys()))
        print("doc_name:", sample_doc.get("doc_name"))
        print("Text snippet:", sample_doc.get("full_text", "")[:200])
        print("Labels (first 3):", list(sample_doc.get("labels", {}).keys())[:3])
    elif isinstance(data, list):
        print("✅ JSON is a list")
        print("Length:", len(data))
        print("Sample keys in first item:", list(data[0].keys()))
    else:
        print("❌ Unexpected JSON format.")

def inspect_csv(path):
    df = pd.read_csv(path)
    print("\n📊 CSV loaded:")
    print("Shape:", df.shape)
    print("Columns (first 5):", df.columns[:5].tolist())
    print("Sample row 0:", df.iloc[0, :5].to_dict())

def inspect_txt_dir(path):
    files = os.listdir(path)
    print(f"\n📁 TXT directory contains {len(files)} files")
    for f in files[:3]:
        print("  -", f)
        sample = open(os.path.join(path, f), encoding="utf8", errors="ignore").readlines()[:2]
        print("    Sample text:", "".join(sample).strip()[:100], "...\n")

if __name__ == "__main__":
    print("🔍 Inspecting CUAD dataset...\n")
    inspect_json(JSON_PATH)
    inspect_csv(CSV_PATH)
    inspect_txt_dir(TXT_DIR)

