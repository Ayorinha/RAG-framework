---
title: "CSVLoader and JSONLLoader for tabular / record-oriented data"
labels: ["enhancement", "good first issue"]
---

## Description

Add two stdlib-only loaders that turn each row / record into a `Document`:

```python
CSVLoader(content_columns=["title", "body"], metadata_columns=["url", "date"], id_column="id")
JSONLLoader(content_key="text", metadata_keys=["source"], id_key="id")
```

## Motivation

FAQ exports, support tickets, product catalogues and scraped datasets almost always arrive as CSV or JSON Lines. These are the cheapest high-value loaders to add.

## Acceptance criteria

- [ ] `CSVLoader(DocumentLoader)` and `JSONLLoader(DocumentLoader)` in `ragframework/document/tabular.py`
- [ ] `content_columns` / `content_key` joined with a configurable separator (default newline); missing columns raise `LoaderError` naming the column and the row number
- [ ] Document id: the value of `id_column` / `id_key` if given, else `f"{_make_id(source)}:{row_index}"`
- [ ] Row index and all `metadata_columns` copied into `Document.metadata`; the whole record is **not** dumped by default
- [ ] `encoding` and `delimiter` (CSV) arguments; malformed JSON lines raise `LoaderError` with the line number
- [ ] Tests with `tmp_path` fixtures for happy path, missing column, bad JSON line, empty file
- [ ] Exported from `ragframework/document/__init__.py`; `CHANGELOG.md` updated

## Files to touch

- `ragframework/document/tabular.py` — new
- `ragframework/document/__init__.py`
- `tests/test_document/test_tabular.py` — new

## Resources

- [`csv.DictReader`](https://docs.python.org/3/library/csv.html#csv.DictReader)
- [JSON Lines](https://jsonlines.org/)

**Estimated effort:** Small (< 2 hours)
