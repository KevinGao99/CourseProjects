import re
from penman import Graph, Triple
from penman.model import Model
from penman.models.noop import NoOpModel
from penman.models import amr

op_model = Model()
noop_model = NoOpModel()
amr_model = amr.model


def get_amr_model(dereify: bool):
    return op_model if dereify else noop_model


def remove_wiki_node(graph: Graph):
    metadata = graph.metadata
    triples = []
    for t in graph.triples:
        v1, rel, v2 = t
        if rel == ':wiki':
            t = Triple(v1, rel, '+')
        triples.append(t)
    graph = Graph(triples)
    graph.metadata = metadata
    return graph


def strip_off_meta(graph: str) -> str:
    lines = graph.split("\n")
    out = []
    for l in lines:
        if not l.startswith("#"):
            out.append(l)
    return "\n".join(out)


def tokenize_penman(graph: str) -> str:
    linearized = re.sub(r"(\".+?\")", r' \1 ', graph)
    pieces = []
    for piece in linearized.split():
        if piece.startswith('"') and piece.endswith('"'):
            pieces.append(piece)
        else:
            piece = piece.replace('(', ' ( ')
            piece = piece.replace(')', ' ) ')
            piece = piece.replace(':', ' :')
            piece = piece.replace('/', ' / ')
            piece = piece.strip()
            pieces.append(piece)
    linearized = re.sub(r'\s+', ' ', ' '.join(pieces)).strip()
    return linearized
