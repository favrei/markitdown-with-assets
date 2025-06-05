# markitdown-ext

`markitdown-ext` is a thin wrapper around [MarkItDown](https://github.com/peterjhsu/markitdown) that saves embedded assets when converting PDFs to Markdown.

## Installation

```bash
uv pip install --index corp markitdown-ext
```

## Usage

Run `markitdownx` with the same arguments you would pass to `markitdown`:

```bash
markitdownx my.pdf -o my.md
```

Attachments extracted from the PDF will be written to `<basename>_assets/`.
