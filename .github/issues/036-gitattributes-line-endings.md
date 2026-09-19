---
title: "Add .gitattributes and normalise mixed CRLF/LF line endings"
labels: ["enhancement", "good first issue"]
---

## Description

21 tracked files have CRLF line endings (`ragframework/document/chunkers.py`, `loaders.py`, `retriever/chroma.py`, `retriever/faiss.py`, `embeddings/huggingface.py`, most tests, `CHANGELOG.md`, `CONTRIBUTING.md`, `.github/workflows/ci.yml`, …) while the rest are LF. There is no `.gitattributes`, so what gets committed depends on each contributor's `core.autocrlf` setting.

## Motivation

Mixed endings cause whole-file diffs, noisy PR reviews and spurious merge conflicts — especially painful with several new contributors on Windows and Linux joining at once.

## Acceptance criteria

- [ ] `.gitattributes` at the repo root:
  ```
  * text=auto eol=lf
  *.png binary
  *.ipynb text eol=lf
  ```
- [ ] Repository renormalised in a single dedicated commit (`git add --renormalize .`) so the change is easy to review and `git blame` can skip it — add that commit's SHA to a new `.git-blame-ignore-revs` file
- [ ] `ruff` / `black` still pass; tests still pass
- [ ] `CONTRIBUTING.md` gets one sentence: line endings are enforced by `.gitattributes`; no local config needed

## Files to touch

- `.gitattributes`, `.git-blame-ignore-revs` — new
- every CRLF file (content unchanged, endings only)
- `CONTRIBUTING.md`

## Resources

- [GitHub: configuring Git to handle line endings](https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings)
- [`blame.ignoreRevsFile`](https://git-scm.com/docs/git-blame#Documentation/git-blame.txt---ignore-revs-fileltfilegt)

**Estimated effort:** Small (< 2 hours)
