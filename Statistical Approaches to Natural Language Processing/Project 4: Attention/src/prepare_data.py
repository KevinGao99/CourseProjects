#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jin Zhao
# Date: 11/14/20 8:59 PM
from typing import Union, List, Optional

import os, re
from pathlib import Path
import click
import penman
from src import TRAIN_PATH, DEV_PATH, TEST_PATH, PROCESSED_DATA_PATH
from src.penman_utils import remove_wiki_node, get_amr_model, strip_off_meta, tokenize_penman
from spacy.lang.en import English
nlp = English()
tokenizer = nlp.tokenizer

UNK = "<unk>"
PAD = "<pad>"
BOS = "<bos>"
EOS = "<eos>"


def ingest_amr_files(folder_path: Union[str, os.PathLike], dereify: bool, remove_wiki: bool) -> List[penman.Graph]:
    out = []
    for file_path in Path(folder_path).iterdir():
        if file_path.suffix.endswith(".txt"):
            graphs = penman.load(file_path, model=get_amr_model(dereify))
            if remove_wiki:
                for i in range(len(graphs)):
                    graphs[i] = remove_wiki_node(graphs[i])
            out.extend(graphs)
    return out


def tokenize_sentence(text: str) -> List[str]:
    tokens = tokenizer(text)
    return [token.text for token in tokens]


def prepare_sentence_files(graphs: List[penman.Graph], out_path: str, out_vocab_path: Optional[str]) -> None:
    vocab = set()
    snts = []
    for g in graphs:
        snt = g.metadata["snt"]
        tokens = tokenize_sentence(snt)
        vocab.update(tokens)
        snts.append(" ".join(tokens))

    with open(out_path, "w") as f:
        f.write("\n".join(snts) + "\n")

    if out_vocab_path:
        with open(out_vocab_path, "w") as f:
            f.write("\n".join([PAD, UNK, BOS, EOS] + list(vocab)))

def recategorize(linearized_tokens):
    recat_tokens = []
    for token in linearized_tokens:
        if re.match(r"\w+-\d+", token):
            recat_tokens.append("-VERB-")
        elif re.match(r'".+"', token):
            recat_tokens.append("-NE-")
        elif re.match(r"\d+", token):
            recat_tokens.append("-NUM-")
        elif re.match(r"\w\d+", token):
            recat_tokens.append(token[0])
        elif len(token) > 1 and ":" not in token:
            recat_tokens.append("-CONCEPT-")
        else:
            recat_tokens.append(token)
    return recat_tokens


def prepare_linearized_graph_files(graphs: List[penman.Graph], out_path: str, out_vocab_path: Optional[str]) -> None:
    vocab = set()
    linearized_lst = []
    for g in graphs:
        g_str = penman.encode(g)
        linearized = tokenize_penman(strip_off_meta(g_str))
        recat_linearized = recategorize(linearized.split())
        vocab.update(recat_linearized)
        linearized_lst.append(" ".join(recat_linearized))

    with open(out_path, "w") as f:
        f.write("\n".join(linearized_lst) + "\n")

    if out_vocab_path:
        with open(out_vocab_path, "w") as f:
            f.write("\n".join([PAD, BOS, EOS] + list(vocab)))


@click.command()
@click.option("--split", "-s", required=True, type=click.Choice(["train", "dev", "test"]))
@click.option("--dereify", "-d", is_flag=True)
@click.option("--remove_wiki", "-r", is_flag=True)
def main(split, dereify, remove_wiki):

    if not os.path.exists(PROCESSED_DATA_PATH):
        os.makedirs(PROCESSED_DATA_PATH)
        print(f"Folder '{PROCESSED_DATA_PATH}' created successfully.")
    else:
        print(f"Folder '{PROCESSED_DATA_PATH}' already exists.")

    splits_dict = {
        "train": TRAIN_PATH,
        "dev": DEV_PATH,
        "test": TEST_PATH,
    }
    graphs = ingest_amr_files(splits_dict[split], dereify, remove_wiki)

    if split == "train":
        prepare_sentence_files(graphs, PROCESSED_DATA_PATH.joinpath(f"{split}_sent.txt"),
                               PROCESSED_DATA_PATH.joinpath("sent_vocab.txt"))
        prepare_linearized_graph_files(graphs, PROCESSED_DATA_PATH.joinpath(f"{split}_graph_gold.txt"),
                                       PROCESSED_DATA_PATH.joinpath("graph_vocab.txt"))
    else:
        prepare_sentence_files(graphs, PROCESSED_DATA_PATH.joinpath(f"{split}_sent.txt"),
                               None)
        prepare_linearized_graph_files(graphs, PROCESSED_DATA_PATH.joinpath(f"{split}_graph_gold.txt"),
                                       None)


if __name__ == '__main__':
    main()
    # e.g., python -m src.prepare_data -s train -d -r
