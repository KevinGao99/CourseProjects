#!/bin/bash
set -eo pipefail

DATA_DIR=$1
MODEL_DIR=$2

if [ -z "$1" ] && [ -z "$2" ]; then
  echo "Data dir and Model dir are required arguments"
  exit 1
fi

params=${@:2}

echo ' ### Prepare Data ###' >&2
python -m src.prepare_data -s train -d -r
python -m src.prepare_data -s dev -d -r
python -m src.prepare_data -s test -d -r


echo ' ### Train ###' >&2
python src/train.py \
  --data_dir $DATA_DIR \
  --model_dir $MODEL_DIR \
  $params

echo ' ### Inference ###' >&2
python src/predict.py \
  --model_dir $MODEL_DIR \
  $params
