# Releasing

Releases are published to PyPI manually from a local machine.

1. Bump the version in `pyproject.toml` and update `CHANGELOG.md`.
2. Build the distribution:
   ```bash
   rm -rf dist build *.egg-info
   python3 -m build
   python3 -m twine check dist/*
   ```
3. Upload to PyPI:
   ```bash
   python3 -m twine upload dist/*
   ```
   Authenticate with username `__token__` and a PyPI API token (`pypi-...`).
4. Tag the release:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
