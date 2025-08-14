from datasets import load_dataset

def main():
    # Pre-download a few common datasets
    for name in ["imdb", "glue", "tweet_eval"]:
        try:
            print("Downloading:", name)
            _ = load_dataset(name)
        except Exception as e:
            print("Failed:", name, e)
    print("Done.")

if __name__ == "__main__":
    main()
