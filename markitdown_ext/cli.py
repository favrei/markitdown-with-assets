"""Entry-point wrapper for markitdown-ext."""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> None:
    """Delegate to the upstream markitdown package."""
    if argv is None:
        argv = sys.argv[1:]

    from markitdown.__main__ import main as upstream_main

    upstream_main(argv)


if __name__ == "__main__":
    main()
