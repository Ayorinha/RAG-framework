---
title: "docs/getting-started.md renders as plain text (escaped headings, HTML entities, 322 blank lines)"
labels: ["bug", "documentation", "good first issue"]
---

## Description

`docs/getting-started.md` appears to have been exported from a rich-text editor. On GitHub it renders as one unformatted blob:

- Every heading is escaped: `\# Getting Started`, `\## Installation`, `\### Requirements` (29 occurrences)
- Indentation inside code blocks is written as `&#x20;` HTML entities
- Underscores are escaped: `chunk\_size`, `top\_k`
- 322 of the 480 lines are blank (every paragraph is separated by 3 empty lines)
- File uses CRLF line endings (see the `.gitattributes` issue)

## Motivation

This is the first document a new contributor or user opens after the README. Right now it is unreadable, which undermines the whole onboarding story.

## Acceptance criteria

- [ ] All `\#` headings converted to real Markdown headings with a sensible hierarchy (`#` → `##` → `###`)
- [ ] `&#x20;` and `\_` escapes removed; code samples are inside fenced ` ```python ` blocks and actually run against the current API
- [ ] Blank-line bloat collapsed to standard single blank lines between paragraphs
- [ ] Content checked against the current codebase: mentions `PDFLoader`, `RecursiveChunker`, `HuggingFaceEmbedder`, `FAISSRetriever`, `ChromaRetriever` where relevant
- [ ] File saved with LF line endings
- [ ] Linked from `README.md` (it currently is not) and from `CONTRIBUTING.md`

## Files to touch

- `docs/getting-started.md`
- `README.md` — add a link under Quick Start
- `CONTRIBUTING.md` — add a link

## Resources

- `README.md` Quick Start and `examples/basic_rag.py` as the source of truth for working code

**Estimated effort:** Small (< 2 hours)
