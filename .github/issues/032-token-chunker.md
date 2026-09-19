---
title: "TokenChunker: split by model tokens instead of characters"
labels: ["enhancement", "good first issue"]
---

## Description

Add `TokenChunker` that measures chunk size in tokens using `tiktoken`, so chunks map directly onto embedding-model and LLM context limits.

```python
TokenChunker(chunk_tokens=256, overlap_tokens=32, encoding_name="cl100k_base")
```

## Motivation

Character counts are a poor proxy: 512 characters is ~128 tokens of English but ~512 tokens of CJK text or code. Every hosted embedding API bills and limits by tokens.

## Acceptance criteria

- [ ] Class `TokenChunker(TextChunker)` in `ragframework/document/chunkers.py`
- [ ] Uses `tiktoken` via a new `[tokens]` extra in `pyproject.toml`; guarded import with the standard install hint
- [ ] Encodes once, slides a token window with overlap, decodes each window back to text; same validation rules as `RecursiveChunker` (`chunk_tokens > 0`, `0 <= overlap < chunk_tokens`)
- [ ] Chunk ids / metadata follow the existing `f"{document.id}:{i}"` + `chunk_index` convention; also store `token_count` in chunk metadata
- [ ] Tests fake the `tiktoken` module (see how `tests/test_embeddings/test_huggingface.py` fakes `sentence_transformers`) so CI needs no download; assert no chunk exceeds `chunk_tokens`
- [ ] Exported from `ragframework/document/__init__.py`; `CHANGELOG.md` updated

## Files to touch

- `ragframework/document/chunkers.py`
- `ragframework/document/__init__.py`
- `pyproject.toml`
- `tests/test_document/test_chunkers.py`

## Resources

- [tiktoken](https://github.com/openai/tiktoken)

**Estimated effort:** Medium (half day)
