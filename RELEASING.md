# Releasing to PyPI

Releases are built and published by [`.github/workflows/release.yml`](.github/workflows/release.yml)
using [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) — no API tokens are stored
anywhere. Pushing a `v*` tag publishes to PyPI; the **Run workflow** button publishes to TestPyPI.

## One-time setup (maintainer)

### 1. Accounts

- Create accounts on <https://pypi.org> and <https://test.pypi.org> (they are separate).
- Enable two-factor authentication on both — PyPI requires it for publishing.

### 2. Register the trusted publisher on PyPI

PyPI → account menu → **Publishing** → *Add a new pending publisher* → **GitHub**:

| Field | Value |
|---|---|
| PyPI project name | `ragframework` |
| Owner | `adaumsilva` |
| Repository name | `RAG-framework` |
| Workflow name | `release.yml` |
| Environment name | `pypi` |

Repeat on **test.pypi.org** with environment name `testpypi`.

"Pending" means the project does not exist yet; the first successful upload creates it and
converts the pending publisher into a normal one.

### 3. Create the GitHub environments

Repo → **Settings → Environments → New environment**:

- `testpypi` — no protection rules needed.
- `pypi` — tick **Required reviewers** and add yourself. Every real release will then pause for
  one click of approval, which is a cheap guard against an accidental tag push.

## Dry run against TestPyPI

Repo → **Actions → Release → Run workflow** (on `main`). When it finishes:

```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ ragframework
python -c "import ragframework; print(ragframework.__version__)"
```

TestPyPI never lets you re-upload the same version, so bump the version (or accept the
`skip-existing` no-op) if you need to test twice.

## Cutting a release

1. Pick the version. Follow [SemVer](https://semver.org/): new features → minor bump,
   fixes only → patch bump, breaking API changes → major bump (or minor while `0.x`).
2. Update the version in **both** places (until #51 single-sources it):
   - `pyproject.toml` → `version = "X.Y.Z"`
   - `ragframework/__init__.py` → `__version__ = "X.Y.Z"`
3. In `CHANGELOG.md`, rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, add a fresh empty
   `## [Unreleased]` above it, and update the two link references at the bottom of the file.
   The release workflow copies this section into the GitHub Release notes.
4. Commit and push to `main`; wait for CI to go green.
5. Tag and push the tag:

   ```bash
   git tag -a vX.Y.Z -m "Release X.Y.Z"
   git push origin vX.Y.Z
   ```

6. Actions → **Release** run: the `build` job checks the tag matches `pyproject.toml`, then
   `publish-pypi` waits for your environment approval. Approve it.
7. Verify:
   - <https://pypi.org/project/ragframework/> shows the new version and a rendered README
   - `pip install ragframework==X.Y.Z` works in a clean virtualenv
   - The GitHub Release was created with the changelog section as notes

## If something goes wrong

- **Tag/version mismatch** — the build job fails before anything is uploaded. Fix the version,
  delete the tag (`git tag -d vX.Y.Z && git push origin :refs/tags/vX.Y.Z`), and tag again.
- **Upload failed after tag** — PyPI never allows re-uploading a version, even a deleted one.
  Bump to the next patch version and release again.
- **`invalid-publisher` error** — the owner / repo / workflow filename / environment name on
  pypi.org does not exactly match the running workflow. Check the table above.
- **Bad release already on PyPI** — you cannot replace it. "Yank" it on pypi.org (Manage →
  release → Options → Yank) so `pip` skips it, then publish a fixed version.

## Manual fallback (no Actions)

```bash
pip install build twine
rm -rf dist && python -m build && twine check dist/*
twine upload dist/*          # username: __token__   password: a pypi.org API token
```
