#!/usr/bin/env bash
export DATASET=imdb
export MODEL_NAME=distilbert-base-uncased
python -m model.train
