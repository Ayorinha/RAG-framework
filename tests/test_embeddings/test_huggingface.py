"""Tests for the HuggingFace Sentence Transformers embedder."""

import builtins
import sys
import types

import numpy as np
import pytest

from ragframework.embeddings.huggingface import HuggingFaceEmbedder
from ragframework.exceptions import EmbedderError


class FakeSentenceTransformer:
    def __init__(self, model_name, device=None):
        self.model_name = model_name
        self.device = device
        self.calls = []

    def encode(self, texts, convert_to_numpy=False):
        self.calls.append((texts, convert_to_numpy))
        return np.asarray([[float(index), 1.0, 2.0] for index, _ in enumerate(texts)])


@pytest.fixture
def fake_sentence_transformers(monkeypatch):
    module = types.ModuleType("sentence_transformers")
    module.SentenceTransformer = FakeSentenceTransformer
    monkeypatch.setitem(sys.modules, "sentence_transformers", module)


def test_default_model_and_optional_device(fake_sentence_transformers):
    default_embedder = HuggingFaceEmbedder()
    device_embedder = HuggingFaceEmbedder("test-model", device="cpu")

    assert default_embedder.model_name == "all-MiniLM-L6-v2"
    assert default_embedder.device is None
    assert default_embedder._model.model_name == "all-MiniLM-L6-v2"
    assert device_embedder._model.model_name == "test-model"
    assert device_embedder._model.device == "cpu"


def test_embed_preserves_count_order_and_dimension(fake_sentence_transformers):
    embedder = HuggingFaceEmbedder()

    vectors = embedder.embed(["first", "second", "third"])

    assert vectors == [[0.0, 1.0, 2.0], [1.0, 1.0, 2.0], [2.0, 1.0, 2.0]]
    assert len(vectors) == 3
    assert {len(vector) for vector in vectors} == {3}
    assert embedder._model.calls == [(["first", "second", "third"], True)]


def test_empty_input_returns_empty_list(fake_sentence_transformers):
    embedder = HuggingFaceEmbedder()

    assert embedder.embed([]) == []
    assert embedder._model.calls == []


def test_missing_dependency_has_helpful_message(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "sentence_transformers":
            raise ImportError("No module named 'sentence_transformers'")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.delitem(sys.modules, "sentence_transformers", raising=False)
    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(
        ImportError, match=r"HuggingFace support requires 'ragframework\[huggingface\]'"
    ):
        HuggingFaceEmbedder()


def test_model_load_failure_raises_embedder_error(monkeypatch):
    class FailingSentenceTransformer:
        def __init__(self, model_name, device=None):
            raise RuntimeError("load failed")

    module = types.ModuleType("sentence_transformers")
    module.SentenceTransformer = FailingSentenceTransformer
    monkeypatch.setitem(sys.modules, "sentence_transformers", module)

    with pytest.raises(EmbedderError, match="Could not load embedding model"):
        HuggingFaceEmbedder("broken-model")


def test_encode_failure_raises_embedder_error(fake_sentence_transformers):
    embedder = HuggingFaceEmbedder()

    def fail_encode(texts, convert_to_numpy=False):
        raise RuntimeError("encode failed")

    embedder._model.encode = fail_encode

    with pytest.raises(EmbedderError, match="Could not create embeddings"):
        embedder.embed(["text"])
