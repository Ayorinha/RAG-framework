---
title: "SentenceChunker: enforce a maximum character length per chunk"
labels: ["enhancement", "good first issue"]
---

## Description

`SentenceChunker` groups N sentences per chunk with no upper bound on characters. A document with three 5 000-character "sentences" yields a single 15 005-character chunk, which will exceed most embedding models' context windows and get truncated silently by the provider.

## Motivation

Chunk size limits are the whole point of chunking. Every other chunker in the package is size-bounded; this one should be too.

## Acceptance criteria

- [ ] New constructor argument `max_chars: int | None = None`. When set, a window that would exceed `max_chars` is closed early (fewer than `max_sentences`), and a single sentence longer than `max_chars` is hard-split at `max_chars` (reuse the fixed-window logic from `FixedSizeChunker`, or delegate to `RecursiveChunker` with `separators=[" ", ""]`)
- [ ] `max_chars <= 0` raises `ValueError`
- [ ] Tests: window closes early; oversized single sentence is split; `None` preserves current behaviour
- [ ] Docstring updated; `CHANGELOG.md` updated under `[Unreleased]` → `### Added`

## Files to touch

- `ragframework/document/chunkers.py` — `SentenceChunker`
- `tests/test_document/test_chunkers.py`

**Estimated effort:** Small (< 2 hours)
