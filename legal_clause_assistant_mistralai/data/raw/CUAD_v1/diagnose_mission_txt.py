import os
import pandas as pd

CSV_PATH = "data/raw/CUAD_v1/master_clauses.csv"
TXT_DIR = "data/raw/CUAD_v1/full_contract_txt/"

def normalize(name):
    return name.replace(".pdf", "").replace(".PDF", "").strip()

def diagnose_missing_files():
    df = pd.read_csv(CSV_PATH)
    all_txt_files = os.listdir(TXT_DIR)
    txt_set = set(f.strip() for f in all_txt_files)

    missing = []
    for fname in df["Filename"]:
        clean = normalize(fname) + ".txt"
        if clean not in txt_set:
            missing.append(clean)

    print(f"🔍 Total missing files: {len(missing)}")
    for i, m in enumerate(missing[:12]):
        print(f"⚠️  Missing: {m}")
        # Suggest similar filenames
        similar = [f for f in txt_set if normalize(f).startswith(normalize(m).split(".txt")[0][:10])]
        if similar:
            print(f"    🔎 Possible match: {similar[0]}")
        else:
            print("    🚫 No similar match found.")

if __name__ == "__main__":
    diagnose_missing_files()

