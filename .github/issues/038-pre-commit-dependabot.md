---
title: "Developer tooling: pre-commit hooks and Dependabot"
labels: ["enhancement", "good first issue"]
---

## Description

Two small additions that keep contributions consistent without maintainer nagging:

1. **`.pre-commit-config.yaml`** running `ruff` (lint + format, or black/isort — match whatever the CI-hardening issue decides), `mypy`, `end-of-file-fixer`, `trailing-whitespace`, `check-yaml`, `check-toml`, `mixed-line-ending --fix=lf`
2. **`.github/dependabot.yml`** for `pip` (weekly, grouped minor/patch) and `github-actions` (weekly)

## Acceptance criteria

- [ ] `.pre-commit-config.yaml` added; `pre-commit` added to `[dev]` extra
- [ ] `pre-commit run --all-files` passes on `main` (fix anything it flags in the same PR)
- [ ] `CONTRIBUTING.md` Development Setup: `pre-commit install` step added
- [ ] `.github/dependabot.yml` added with the two ecosystems, `open-pull-requests-limit` set, and a `groups:` block so minor/patch bumps arrive as one PR

## Files to touch

- `.pre-commit-config.yaml`, `.github/dependabot.yml` — new
- `pyproject.toml`
- `CONTRIBUTING.md`

## Resources

- [pre-commit](https://pre-commit.com/)
- [ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit)
- [Dependabot configuration options](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)

**Estimated effort:** Small (< 2 hours)
