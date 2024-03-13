#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jayeol Chun
# Date: 11/15/20 4:24 AM
import logging

logger = logging.getLogger(__name__)

from pathlib import Path

RAW_DATA_PATH = Path(__file__).parent.parent.joinpath("amr_anno_1.0")
TRAIN_PATH = RAW_DATA_PATH.joinpath("data/split/training")
DEV_PATH = RAW_DATA_PATH.joinpath("data/split/dev")
TEST_PATH = RAW_DATA_PATH.joinpath("data/split/test")

OUTPUT_PATH = Path(__file__).parent.parent.joinpath("outputs")
PROCESSED_DATA_PATH = OUTPUT_PATH.joinpath("processed_data")



def main():
  pass

if __name__ == '__main__':
  main()
