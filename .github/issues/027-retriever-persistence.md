---
title: "Persist and reload FAISSRetriever and InMemoryRetriever indexes"
labels: ["enhancement", "good first issue"]
---

## Description

Only `ChromaRetriever` survives a process restart. `FAISSRetriever` and `InMemoryRetriever` must re-embed the whole corpus every run. Add:

```python
retriever.save("index_dir/")
retriever = FAISSRetriever.load("index_dir/")
```

## Motivation

Embedding is the slow, expensive step (API cost or GPU time). Losing the index on exit makes the two fastest retrievers impractical beyond demos.

## Acceptance criteria

- [ ] `save(path: str | Path) -> None` and `@classmethod load(path) -> Self` on both classes
- [ ] `FAISSRetriever.save` writes `index.faiss` (`faiss.write_index`) + `chunks.json` (ids, content, metadata) + `meta.json` (dimension, `m`, `ef_construction`, `ef_search`, format version)
- [ ] `InMemoryRetriever.save` writes `matrix.npy` + `chunks.json`
- [ ] Use JSON, **not pickle**, for chunk data (safe to load untrusted files); `np.load(..., allow_pickle=False)`
- [ ] `load()` on a missing/corrupt directory raises `RetrieverError`; format-version mismatch raises `RetrieverError` with guidance
- [ ] Round-trip tests with `tmp_path`: save → load → identical `len()` and identical `retrieve()` results
- [ ] Docstrings + `examples/README.md` snippet; `CHANGELOG.md` updated

## Files to touch

- `ragframework/retriever/faiss.py`
- `ragframework/retriever/in_memory.py`
- `tests/test_retriever/test_faiss.py`, `tests/test_retriever/test_in_memory.py`
- `examples/README.md`

## Resources

- [`faiss.write_index` / `read_index`](https://github.com/facebookresearch/faiss/wiki/Index-IO,-cloning-and-hyper-parameter-tuning)
- [`numpy.save` / `numpy.load`](https://numpy.org/doc/stable/reference/generated/numpy.save.html)

**Estimated effort:** Medium (half day)
