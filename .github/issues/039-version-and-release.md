---
title: "Single-source the version and add a PyPI release workflow"
labels: ["enhancement", "help wanted"]
---

## Description

The version is declared twice — `pyproject.toml` (`version = "0.1.0"`) and `ragframework/__init__.py` (`__version__ = "0.1.0"`) — and will drift. There is also no release automation; the README says "Once published to PyPI, installation will simplify to `pip install ragframework`", so publishing is the goal.

## Acceptance criteria

- [ ] `ragframework/__init__.py` derives `__version__` from `importlib.metadata.version("ragframework")` (with a `PackageNotFoundError` fallback of `"0.0.0+unknown"` for source checkouts that aren't installed); `pyproject.toml` remains the single source of truth
- [ ] Test that `ragframework.__version__` matches the installed metadata
- [ ] `.github/workflows/release.yml` triggered on `v*` tags: builds sdist + wheel with `python -m build`, runs `twine check`, publishes with **PyPI Trusted Publishing** (`pypa/gh-action-pypi-publish`, `permissions: id-token: write`, no long-lived secrets), and creates a GitHub Release with notes extracted from the matching `CHANGELOG.md` section
- [ ] `CONTRIBUTING.md` / a short `RELEASING.md`: bump version in `pyproject.toml` → move `[Unreleased]` to a dated section → tag → push
- [ ] Maintainer action required (not in the PR): register the project on PyPI and configure the trusted publisher for this repo/workflow
- [ ] README install instructions updated once the first release is out

## Files to touch

- `ragframework/__init__.py`
- `.github/workflows/release.yml` — new
- `RELEASING.md` — new (or a section in `CONTRIBUTING.md`)
- `tests/test_version.py` — new

## Resources

- [`importlib.metadata`](https://docs.python.org/3/library/importlib.metadata.html)
- [Publishing to PyPI with Trusted Publishing](https://docs.pypi.org/trusted-publishers/using-a-publisher/)
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)

**Estimated effort:** Medium (half day)
