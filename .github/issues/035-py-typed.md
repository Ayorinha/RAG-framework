---
title: "Ship a py.typed marker so downstream users get type hints (PEP 561)"
labels: ["enhancement", "good first issue"]
---

## Description

The package is type-checked with `mypy --strict` in CI, but there is no `ragframework/py.typed` file, so mypy/pyright in **user** projects treat `ragframework` as untyped and ignore all the annotations.

## Acceptance criteria

- [ ] Empty file `ragframework/py.typed` added
- [ ] `pyproject.toml`: `[tool.setuptools.package-data] ragframework = ["py.typed"]` so it is included in wheels
- [ ] `"Typing :: Typed"` added to `classifiers`
- [ ] Verified by building a wheel (`pip install build && python -m build`) and confirming `py.typed` is inside it (`unzip -l dist/*.whl | grep py.typed`)
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Added`

## Files to touch

- `ragframework/py.typed` — new (empty)
- `pyproject.toml`

## Resources

- [PEP 561](https://peps.python.org/pep-0561/)
- [setuptools package data](https://setuptools.pypa.io/en/latest/userguide/datafiles.html)

**Estimated effort:** Small (< 2 hours)
