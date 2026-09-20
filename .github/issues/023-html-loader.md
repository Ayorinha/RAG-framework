---
title: "HTMLLoader for local .html files and web URLs"
labels: ["enhancement", "good first issue"]
---

## Description

Add `HTMLLoader` that extracts readable text from an HTML file or URL, dropping `<script>`, `<style>`, `<nav>` and similar, and returns a single `Document` with `title` in metadata.

## Motivation

Documentation sites, wikis and exported web pages are a primary RAG corpus. Nothing in the framework can ingest them today.

## Acceptance criteria

- [ ] Class `HTMLLoader(DocumentLoader)` in `ragframework/document/html.py`
- [ ] Works with **zero extra dependencies** using `html.parser.HTMLParser` from the stdlib; if `beautifulsoup4` is installed it may be used for better results (guarded import, new `[html]` extra in `pyproject.toml`)
- [ ] `source` may be a local path or an `http(s)://` URL (`urllib.request` with a timeout and a custom `User-Agent`); network failures raise `LoaderError`
- [ ] Skips `script`, `style`, `noscript`, `template`, `head`; collapses whitespace via `ragframework.utils.text.normalize_whitespace`
- [ ] Metadata: `source`, `title` (from `<title>`), `format: "html"`
- [ ] Tests use local fixture files only — no live network calls in CI (mock `urlopen` for the URL path)
- [ ] Exported from `ragframework/document/__init__.py`; `CHANGELOG.md` updated

## Files to touch

- `ragframework/document/html.py` — new
- `ragframework/document/__init__.py`
- `pyproject.toml` — optional `[html]` extra
- `tests/test_document/test_html.py` — new

## Resources

- [`html.parser`](https://docs.python.org/3/library/html.parser.html)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

**Estimated effort:** Medium (half day)
