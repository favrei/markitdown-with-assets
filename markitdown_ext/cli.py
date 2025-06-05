"""Entry-point wrapper for markitdown-ext."""

from __future__ import annotations

import argparse
import os
import sys


def main(argv: list[str] | None = None) -> None:
    """Convert a PDF to Markdown and persist attachments."""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="markitdownx")
    parser.add_argument("input_pdf")
    parser.add_argument("output_md")
    args = parser.parse_args(argv)

    from markitdown import MarkItDown

    md = MarkItDown()
    result = md.convert(args.input_pdf, args.output_md)

    attachments = getattr(result, "attachments", {})
    if attachments:
        assets_dir = os.path.splitext(args.output_md)[0] + "_assets"
        os.makedirs(assets_dir, exist_ok=True)
        for name, data in attachments.items():
            with open(os.path.join(assets_dir, name), "wb") as f:
                f.write(data)


if __name__ == "__main__":
    main()
