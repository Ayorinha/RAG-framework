---
title: "TextFileLoader / MarkdownLoader leak UnicodeDecodeError instead of LoaderError"
labels: ["bug", "good first issue"]
---

## Description

Both file loaders only catch `OSError` around `path.read_text(...)`. A file that is not valid in the configured encoding raises a raw `UnicodeDecodeError` (a `ValueError`), and an unknown encoding name raises `LookupError`:

```python
TextFileLoader().load("latin1.txt")            # UnicodeDecodeError
TextFileLoader(encoding="nope").load("a.txt")  # LookupError
```

The documented contract (`ragframework/exceptions.py`, `CONTRIBUTING.md`) is that loaders raise `LoaderError`.

## Motivation

Callers that catch `LoaderError` (or `RAGFrameworkError`) miss these failures. The pipeline still wraps them in `PipelineError`, but direct loader users do not get the promised exception type.

## Acceptance criteria

- [ ] `UnicodeDecodeError` and `LookupError` are converted to `LoaderError` with the file path and encoding in the message
- [ ] The duplicated exists / is_file / read_text block in `TextFileLoader` and `MarkdownLoader` is extracted into a private helper (e.g. `_read_text_file(path, encoding)`) so the fix lives in one place
- [ ] Optional: `errors: str = "strict"` constructor argument passed through to `read_text` so users can opt into `"replace"`
- [ ] Tests for both failure modes in `tests/test_document/test_loaders.py`
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Fixed`

## Files to touch

- `ragframework/document/loaders.py` — `TextFileLoader.load`, `MarkdownLoader.load`
- `tests/test_document/test_loaders.py`

## Resources

- [`Path.read_text`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.read_text)
- [Error handlers](https://docs.python.org/3/library/codecs.html#error-handlers)

**Estimated effort:** Small (< 2 hours)
