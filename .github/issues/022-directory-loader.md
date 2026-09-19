---
title: "DirectoryLoader: ingest a whole folder with per-extension loader dispatch"
labels: ["enhancement", "good first issue"]
---

## Description

Add `DirectoryLoader` that walks a directory (optionally recursive, with glob filtering) and delegates each file to the right loader by extension, returning the concatenated `list[Document]`.

```python
loader = DirectoryLoader(
    loaders={".txt": TextFileLoader(), ".md": MarkdownLoader(), ".pdf": PDFLoader()},
    glob="**/*",
    recursive=True,
    on_error="skip",   # or "raise"
)
pipeline = RAGPipeline(loader=loader, ...)
pipeline.ingest("./knowledge_base")
```

## Motivation

Today `RAGPipeline.ingest()` takes a single file path, so indexing a corpus means writing a loop by hand and choosing loaders manually. This is the single most requested convenience in every RAG library.

## Acceptance criteria

- [ ] Class `DirectoryLoader(DocumentLoader)` in `ragframework/document/loaders.py`
- [ ] Sensible default `loaders` mapping (`.txt`, `.md`, `.markdown`, `.pdf` when `pypdf` is importable) built lazily so importing the module never requires optional deps
- [ ] Files with no matching loader are skipped (and counted); `on_error="raise"` re-raises as `LoaderError` with the offending path
- [ ] `source` must be an existing directory, otherwise `LoaderError`
- [ ] Deterministic ordering (sorted paths) so chunk ids are stable across runs
- [ ] Each `Document.metadata` includes `"relative_path"` from the root directory
- [ ] Tests using `tmp_path` with mixed extensions, nested folders, an unreadable file with both `on_error` modes
- [ ] Exported from `ragframework/document/__init__.py`; `CHANGELOG.md` updated

## Files to touch

- `ragframework/document/loaders.py`
- `ragframework/document/__init__.py`
- `tests/test_document/test_loaders.py`

## Resources

- [`Path.rglob`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.rglob)

**Estimated effort:** Medium (half day)
