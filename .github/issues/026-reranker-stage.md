---
title: "Add an optional Reranker stage to the pipeline (ABC + cross-encoder implementation)"
labels: ["enhancement", "help wanted"]
---

## Description

Introduce a `Reranker` ABC and wire it into `RAGPipeline.query()` between retrieval and generation:

```python
class Reranker(ABC):
    @abstractmethod
    def rerank(self, query: str, chunks: list[Chunk], top_k: int) -> list[Chunk]: ...
```

Pipeline flow becomes: embed query → retrieve `config.retrieve_k` (e.g. 20) → rerank to `config.top_k` (e.g. 5) → generate.

## Motivation

Two-stage retrieval (cheap bi-encoder recall, precise cross-encoder precision) is the standard way to lift RAG answer quality by a large margin, and it fits the framework's plug-in architecture perfectly.

## Acceptance criteria

- [ ] `Reranker` ABC in `ragframework/base.py`; `RerankerError` in `ragframework/exceptions.py`
- [ ] `RAGPipeline.__init__(..., reranker: Reranker | None = None)`; `RAGConfig.retrieve_k: int | None = None` (defaults to `top_k` when no reranker is set, or `top_k * 4` when one is)
- [ ] `CrossEncoderReranker` in `ragframework/reranker/cross_encoder.py` using `sentence_transformers.CrossEncoder` (already covered by the `[huggingface]` extra; default model `cross-encoder/ms-marco-MiniLM-L-6-v2`), guarded import following the `HuggingFaceEmbedder` pattern
- [ ] A dependency-free `NoOpReranker` for tests
- [ ] Sets `Chunk.score` if the retrieval-scores issue has landed, otherwise stores the rerank score in `metadata["rerank_score"]`
- [ ] Pipeline test with a fake reranker that reverses order, asserting the generator receives the reranked list
- [ ] `README.md` architecture section and `CHANGELOG.md` updated

## Files to touch

- `ragframework/base.py`, `ragframework/exceptions.py`, `ragframework/config.py`
- `ragframework/pipeline/rag.py`
- `ragframework/reranker/__init__.py`, `ragframework/reranker/cross_encoder.py` — new
- `tests/test_reranker/`, `tests/test_pipeline/test_rag.py`

## Resources

- [Sentence Transformers cross-encoders](https://www.sbert.net/docs/cross_encoder/usage/usage.html)
- `tests/test_embeddings/test_huggingface.py` for how to fake `sentence_transformers` in tests

**Estimated effort:** Medium (half day)
