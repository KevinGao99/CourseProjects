#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jayeol Chun, Modified by: Jin Zhao
# Date: 11/28/23 2:05 AM
"""Constants"""
from typing import Dict, List, Tuple

# File names
ARGS_JSON_FILENAME = 'args.json'
SENT_VOCAB_FILENAME = 'sent_vocab.txt'
GRAPH_VOCAB_FILENAME = 'graph_vocab.txt'

# File name formatters
SENT_DATA_FORMATTER = '{}_sent.txt'
GRAPH_DATA_FORMATTER = '{}_graph_gold.txt'
GRAPH_PRED_FORMATTER = '{}_graph_pred.txt'
MODEL_PT_FORMATTER = 'model_{:.2f}.pt'

# Vocab special symbols
PAD = '<pad>' # padding token
UNK = '<unk>' # unknown token
BOS = '<bos>' # beginning of sequence
EOS = '<eos>' # end of sequence
SPECIAL_SYMBOLS = [PAD, UNK, BOS, EOS]

GRU = 'gru'
LSTM = 'lstm'

# Official AMR dataset split names
AMR_SPLITS = ['dev', 'train', 'test']

# Flags to ignore when comparing two argparse Namespaces
DATA_IGNORE_FLAGS = ['force']
TRAIN_IGNORE_FLAGS = ['seed', 'resume_training', 'force', 'epochs', 'eval_every',
                      'batch_size', 'learning_rate', 'teacher_forcing_ratio']
IGNORE_FLAGS = DATA_IGNORE_FLAGS + TRAIN_IGNORE_FLAGS

# Data Types
SENTS_T = List[str]
GRAPHS_T = List[str]
DATASET_T = Tuple[SENTS_T, GRAPHS_T]
ITOS_T = List[str]
STOI_T = Dict[str, int]
VOCAB_T = Tuple[ITOS_T, STOI_T]
VOCABS_T = Tuple[VOCAB_T, VOCAB_T]
