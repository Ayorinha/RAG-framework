---
title: "Promote __len__ and add clear() to the Retriever ABC"
labels: ["enhancement", "good first issue"]
---

## Description

All three built-in retrievers implement `__len__`, but it is not part of the `Retriever` ABC, so generic code (`if len(pipeline.retriever) == 0: ...`) is not type-safe and third-party retrievers are not required to provide it. There is also no way to empty an index short of constructing a new retriever.

## Acceptance criteria

- [ ] `Retriever.__len__(self) -> int` declared `@abstractmethod` in `ragframework/base.py` with a docstring ("number of indexed chunks")
- [ ] `Retriever.clear(self) -> None` declared `@abstractmethod`; implemented in `InMemoryRetriever` (reset list + matrix), `FAISSRetriever` (drop index + dimension so the next `add` rebuilds), `ChromaRetriever` (delete + recreate the collection)
- [ ] `CONTRIBUTING.md` "Adding a New Integration" section updated to list the new required methods
- [ ] Tests: `clear()` → `len() == 0` and `retrieve()` returns `[]`; re-`add` after clear works (FAISS dimension may differ after clear)
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Changed` (note: breaking for third-party `Retriever` subclasses)

## Files to touch

- `ragframework/base.py`
- `ragframework/retriever/in_memory.py`, `faiss.py`, `chroma.py`
- `CONTRIBUTING.md`
- `tests/test_retriever/*`

**Estimated effort:** Small (< 2 hours)
