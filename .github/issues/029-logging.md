---
title: "Add structured logging across pipeline stages"
labels: ["enhancement", "good first issue"]
---

## Description

The package emits no log output at all. Add a module-level logger (`logging.getLogger("ragframework")`) and log at each pipeline stage:

- `ingest`: source, number of documents loaded, number of chunks produced, embedding time, chunks indexed. `WARNING` when a source yields zero chunks (currently `ingest()` just returns `0` silently)
- `query`: `top_k`, number of chunks retrieved, retrieval + generation time
- Retrievers: `DEBUG` on add (count, dimension)

## Motivation

When retrieval returns nothing useful, users currently have no way to tell whether the document loaded empty, chunked into nothing, or the embedder returned junk. Standard-library logging with a `NullHandler` is the idiomatic, zero-cost way to give them visibility.

## Acceptance criteria

- [ ] `ragframework/__init__.py` attaches `logging.NullHandler()` to the `"ragframework"` logger (library best practice — never configure handlers for the user)
- [ ] Each module uses `logger = logging.getLogger(__name__)` (so users can filter `ragframework.retriever.faiss` etc.)
- [ ] Levels: `INFO` for stage summaries, `DEBUG` for per-batch detail, `WARNING` for empty ingest — no `print()` anywhere in `ragframework/`
- [ ] Tests use `caplog` to assert the empty-ingest warning and the ingest summary
- [ ] `docs/getting-started.md` (or README) shows the two-line `logging.basicConfig(level=logging.INFO)` snippet to enable output
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Added`

## Files to touch

- `ragframework/__init__.py`
- `ragframework/pipeline/rag.py`
- `ragframework/retriever/*.py`
- `tests/test_pipeline/test_rag.py`

## Resources

- [Configuring logging for a library](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library)

**Estimated effort:** Small (< 2 hours)
