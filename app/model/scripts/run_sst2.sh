#!/usr/bin/env bash
export DATASET=glue
export TASK_NAME=sst2
export MODEL_NAME=distilbert-base-uncased
python -m model.train
