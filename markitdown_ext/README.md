# markitdown-ext

`markitdown-ext` is a thin wrapper around [MarkItDown](https://github.com/peterjhsu/markitdown) that saves embedded assets when converting PDFs to Markdown.

## Usage

Install the package and run `markitdownx` with the same arguments you would pass to `markitdown`:

```bash
markitdownx input.pdf output.md
```

Attachments extracted from the PDF will be written to `<output>_assets/`.
