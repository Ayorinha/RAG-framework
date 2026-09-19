---
title: "CI hardening: Python 3.13/3.14, format checks, lint tests/, mypy on all versions, coverage floor"
labels: ["enhancement", "good first issue"]
---

## Description

`.github/workflows/ci.yml` currently:

- tests only Python 3.10–3.12 (3.13 has been stable for a year; contributors are already on 3.14)
- runs `ruff check ragframework/` only — `tests/` and `examples/` are never linted
- never runs `black --check` or `isort --check-only` although both are in `[dev]` and documented in `CONTRIBUTING.md`
- runs mypy only on 3.10
- uploads coverage but enforces no minimum (`fail_ci_if_error: false`, no `--cov-fail-under`)
- does not install the `[pdf]` extra, so `PDFLoader` is only exercised through a fake `pypdf`

## Acceptance criteria

- [ ] Matrix extended to `["3.10", "3.11", "3.12", "3.13", "3.14"]`; classifiers in `pyproject.toml` updated to match; `black`/`ruff` `target-version` lists updated
- [ ] Separate fast `lint` job: `ruff check .` plus either `ruff format --check .` **or** `black --check . && isort --check-only .` (pick one formatter; if ruff-format, drop black/isort from `[dev]` and update `CONTRIBUTING.md`)
- [ ] `mypy ragframework/` runs on the oldest and newest Python in the matrix
- [ ] `pytest --cov-fail-under=85` (measure the current number first and set the floor just below it)
- [ ] `[pdf]` added to the CI install so at least one real-`pypdf` test can run (a tiny generated PDF fixture via `pypdf.PdfWriter`)
- [ ] `concurrency:` block added so superseded PR runs are cancelled
- [ ] Any failures the wider lint surfaces are fixed in the same PR

## Files to touch

- `.github/workflows/ci.yml`
- `pyproject.toml`
- `CONTRIBUTING.md`
- possibly `tests/` and `examples/` (lint fixes)

## Resources

- [actions/setup-python](https://github.com/actions/setup-python)
- [pytest-cov `--cov-fail-under`](https://pytest-cov.readthedocs.io/en/latest/config.html)

**Estimated effort:** Medium (half day)
