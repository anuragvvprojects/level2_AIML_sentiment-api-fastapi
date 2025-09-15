import json
from collections import defaultdict

CUAD_PATH = "data/raw/CUADv1.json"

def analyze_cuad_file(path):
    with open(path, "r") as f:
        data = json.load(f)

    print("✅ Top-level keys in CUAD file:", list(data.keys()))

    if "data" not in data or not isinstance(data["data"], list):
        print("❌ 'data' is missing or not a list.")
        return

    contracts = data["data"]
    print(f"📄 Total contracts found: {len(contracts)}")

    # Print sample contract info
    for i, doc in enumerate(contracts):
        print(f"\n📑 Sample Document #{i+1}")
        print("🔹 Keys:", list(doc.keys()))
        print("🔹 doc_name:", doc.get("doc_name", "N/A"))
        print("🔹 Text snippet:", doc.get("full_text", "")[:200], "...")

        labels = doc.get("labels", {})
        print("🔹 Clause types:", list(labels.keys())[:5], "...")
        break  # Show only the first document

    # Count clause type frequency
    clause_counter = defaultdict(int)
    for doc in contracts:
        for clause, spans in doc.get("labels", {}).items():
            if spans:
                clause_counter[clause] += 1

    print("\n📊 Top Clause Types:")
    for clause, count in sorted(clause_counter.items(), key=lambda x: -x[1])[:10]:
        print(f"   {clause}: {count} documents")

if __name__ == "__main__":
    analyze_cuad_file(CUAD_PATH)
