# markitdown-ext

A thin wrapper around the [MarkItDown](https://github.com/peterjhsu/markitdown) CLI that preserves embedded assets when converting PDFs to Markdown.

See [instruction.md](instruction.md) for the original product requirements document.

This repository is meant to be used with the [uv](https://github.com/astral-sh/uv) package manager.

## Running from source

Create a virtual environment and install the project in editable mode:

```bash
uv venv
uv pip install -e .
```

Execute the CLI with `uv run`:

```bash
uv run python -m markitdown_ext.cli example.pdf -o example.md
```

## Running tests

Install the test dependencies and execute pytest via `uv run`:

```bash
uv pip install pytest
uv run python -m pytest -q
```

## Publishing a release

Pushing a version tag triggers the GitHub Actions workflow defined in [publish.yml](.github/workflows/publish.yml).
The workflow runs `uv build --no-sources` and `uv publish --index corp` to upload the wheel to the internal registry.
You can create a release locally with:

```bash
git tag v0.1.0
uv build --no-sources
uv publish --index corp
```

Then push the tag to GitHub to store the artifacts in the release:

```bash
git push origin v0.1.0
```

## Installing the released package

Colleagues with access to this repository can fetch the latest published wheel using uv:

```bash
uv pip install --index corp markitdown-ext
```

## Using the tool

After installation the command `markitdownx` is available:

```bash
uv run markitdownx my.pdf -o my.md
```

Extracted assets will be written to `my_assets/` next to the output Markdown file.

## Verifying a release

The CI job publishes the wheel and then attempts an install of the exact tag to confirm it is available:

```bash
uv pip install --index corp markitdown-ext==${{ github.ref_name }}
```

If this step succeeds the release is considered valid.
