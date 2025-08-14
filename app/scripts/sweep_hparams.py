import itertools, os, subprocess

MODELS = ["distilbert-base-uncased", "bert-base-uncased"]
LRS = ["5e-5", "3e-5"]
BATCH = ["8", "16"]

for m, lr, bs in itertools.product(MODELS, LRS, BATCH):
    env = os.environ.copy()
    env["MODEL_NAME"] = m
    env["LR"] = lr
    env["BATCH_SIZE"] = bs
    print("Running", m, lr, bs)
    subprocess.run(["python", "-m", "model.train"], env=env, check=False)
