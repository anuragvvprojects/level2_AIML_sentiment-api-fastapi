import os
import pandas as pd

CSV_PATH = "data/raw/CUAD_v1/master_clauses.csv"
TXT_DIR = "data/raw/CUAD_v1/full_contract_txt/"

def check_master_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        print("✅ master_clauses.csv loaded successfully.")
        print(f"📊 Shape: {df.shape}")
        print("📄 First 5 columns:", df.columns[:5].tolist())
        print("📝 Sample row:", df.iloc[0, :5].to_dict())
        return df
    except Exception as e:
        print("❌ Error loading CSV:", e)
        return None

def check_txt_files(txt_dir, df):
    if not os.path.exists(txt_dir):
        print("❌ TXT directory does not exist.")
        return

    txt_files = os.listdir(txt_dir)
    txt_files_set = set(txt_files)  # For faster lookup

    print(f"📁 Found {len(txt_files)} TXT files.")

    missing_files = []
    matched_files = 0

    for fname in df["Filename"]:
        clean_name = fname.replace(".pdf", "").replace(".PDF", "")
        txt_file = f"{clean_name}.txt"
        if txt_file in txt_files_set:
            matched_files += 1
        else:
            missing_files.append(txt_file)

    print(f"✅ {matched_files} matching TXT files found.")
    if missing_files:
        print(f"⚠️ Missing {len(missing_files)} TXT files. Sample missing:", missing_files[:5])
    else:
        print("🎉 All TXT files accounted for.")
        
        
if __name__ == "__main__":
    print("Testing CUAD master CSV and TXT document alignment")
    df = check_master_csv(CSV_PATH)
    if df is not None:
        check_txt_files(TXT_DIR, df)
