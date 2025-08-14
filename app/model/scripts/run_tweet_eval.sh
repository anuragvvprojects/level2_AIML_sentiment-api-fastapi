#!/usr/bin/env bash
export DATASET=tweet_eval
export MODEL_NAME=distilbert-base-uncased
python -m model.train
