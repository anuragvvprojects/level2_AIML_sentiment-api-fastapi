#!/usr/bin/env bash
export MODEL_NAME=${MODEL_NAME:-distilbert-base-uncased}
export DATASET=${DATASET:-imdb}
python -m model.train
