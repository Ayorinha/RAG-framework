---
title: "README roadmap, GOOD_FIRST_ISSUES.md and CHANGELOG are out of date"
labels: ["documentation", "good first issue"]
---

## Description

Several docs still describe the v0.1.0 state:

- **`README.md` Roadmap table** marks PDF loader, HuggingFace embedder, FAISS, ChromaDB, recursive chunker and Jupyter notebook as `Open` — all six are merged (issues #1, #3, #4, #5, #7, #10 closed)
- **`.github/GOOD_FIRST_ISSUES.md`** says issues "will be opened" and lists the same six finished items as available work; it also duplicates the content of `.github/issues/*.md`, so it drifts every time an issue file changes
- **`CHANGELOG.md`** `[Unreleased]` section: missing blank line before `## [0.1.0]`, and two entries lack backticks (`RecursiveChunker`, `PDFLoader`) unlike the others
- **`examples/README.md`** says OpenAI integrations "are not included" — still true, but it should point at the open issues (#6, #8, #20) instead of the stale good-first-issues file
- Ten source docstrings reference `.github/GOOD_FIRST_ISSUES.md` (e.g. `InMemoryRetriever`, `EchoGenerator`, `RandomEmbedder`, `loaders.py`, `chunkers.py`) — they should link to the GitHub issues page instead so they don't rot

## Acceptance criteria

- [ ] Roadmap table reflects reality (Done / Open / In progress) and links each row to its issue number
- [ ] `GOOD_FIRST_ISSUES.md` becomes a short pointer: how to find issues (`label:"good first issue"` link), how to claim one, link to `CONTRIBUTING.md`. Detailed specs live only in `.github/issues/*.md` + GitHub
- [ ] `CHANGELOG.md` formatting fixed
- [ ] Docstring references updated to `https://github.com/adaumsilva/RAG-framework/issues`
- [ ] `examples/README.md` links to the open integration issues

## Files to touch

- `README.md`
- `.github/GOOD_FIRST_ISSUES.md`
- `CHANGELOG.md`
- `examples/README.md`
- `ragframework/document/loaders.py`, `ragframework/document/chunkers.py`, `ragframework/embeddings/random_embedder.py`, `ragframework/retriever/in_memory.py`, `ragframework/generator/echo_generator.py`

**Estimated effort:** Small (< 2 hours)
