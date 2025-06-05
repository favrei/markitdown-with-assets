"""Command line interface for markitdown-ext.

This module mirrors the upstream ``markitdown`` CLI but saves
any attachments returned by ``MarkItDown`` to disk.
"""

from __future__ import annotations

import argparse
import codecs
import sys
from pathlib import Path
from textwrap import dedent
from importlib.metadata import entry_points

from markitdown.__about__ import __version__
from markitdown._markitdown import MarkItDown, StreamInfo, DocumentConverterResult


def _exit_with_error(message: str) -> None:
    print(message)
    sys.exit(1)


def _handle_output(args: argparse.Namespace, result: DocumentConverterResult) -> None:
    """Write result.markdown to stdout or ``args.output``."""
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result.markdown)
    else:
        print(
            result.markdown.encode(sys.stdout.encoding, errors="replace").decode(
                sys.stdout.encoding
            )
        )


def _write_attachments(filename: str | None, result: DocumentConverterResult) -> None:
    """Persist attachments to ``<stem>_assets/`` and rewrite markdown links."""
    attachments = getattr(result, "attachments", None)
    if not attachments:
        return

    stem = Path(filename or "stdin").stem
    assets_dir = Path(f"{stem}_assets")
    assets_dir.mkdir(parents=True, exist_ok=True)

    markdown = result.markdown
    for name, data in attachments.items():
        path = assets_dir / name
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        markdown = markdown.replace(name, str(path))

    result.markdown = markdown


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Convert various file formats to markdown.",
        prog="markitdownx",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=dedent(
            """
            SYNTAX:

                markitdownx <OPTIONAL: FILENAME>
                If FILENAME is empty, markitdownx reads from stdin.

            EXAMPLE:

                markitdownx example.pdf

                OR

                cat example.pdf | markitdownx

                OR

                markitdownx < example.pdf

                OR to save to a file use

                markitdownx example.pdf -o example.md

                OR

                markitdownx example.pdf > example.md
            """
        ).strip(),
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show the version number and exit",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file name. If not provided, output is written to stdout.",
    )

    parser.add_argument(
        "-x",
        "--extension",
        help="Provide a hint about the file extension (e.g., when reading from stdin).",
    )

    parser.add_argument(
        "-m",
        "--mime-type",
        help="Provide a hint about the file's MIME type.",
    )

    parser.add_argument(
        "-c",
        "--charset",
        help="Provide a hint about the file's charset (e.g, UTF-8).",
    )

    parser.add_argument(
        "-d",
        "--use-docintel",
        action="store_true",
        help="Use Document Intelligence to extract text instead of offline conversion. Requires a valid Document Intelligence Endpoint.",
    )

    parser.add_argument(
        "-e",
        "--endpoint",
        type=str,
        help="Document Intelligence Endpoint. Required if using Document Intelligence.",
    )

    parser.add_argument(
        "-p",
        "--use-plugins",
        action="store_true",
        help="Use 3rd-party plugins to convert files. Use --list-plugins to see installed plugins.",
    )

    parser.add_argument(
        "--list-plugins",
        action="store_true",
        help="List installed 3rd-party plugins. Plugins are loaded when using the -p or --use-plugin option.",
    )

    parser.add_argument(
        "--keep-data-uris",
        action="store_true",
        help="Keep data URIs (like base64-encoded images) in the output. By default, data URIs are truncated.",
    )

    parser.add_argument("filename", nargs="?")
    args = parser.parse_args(argv)

    extension_hint = args.extension
    if extension_hint is not None:
        extension_hint = extension_hint.strip().lower()
        if len(extension_hint) > 0:
            if not extension_hint.startswith("."):
                extension_hint = "." + extension_hint
        else:
            extension_hint = None

    mime_type_hint = args.mime_type
    if mime_type_hint is not None:
        mime_type_hint = mime_type_hint.strip()
        if len(mime_type_hint) > 0:
            if mime_type_hint.count("/") != 1:
                _exit_with_error(f"Invalid MIME type: {mime_type_hint}")
        else:
            mime_type_hint = None

    charset_hint = args.charset
    if charset_hint is not None:
        charset_hint = charset_hint.strip()
        if len(charset_hint) > 0:
            try:
                charset_hint = codecs.lookup(charset_hint).name
            except LookupError:
                _exit_with_error(f"Invalid charset: {charset_hint}")
        else:
            charset_hint = None

    stream_info = None
    if extension_hint is not None or mime_type_hint is not None or charset_hint is not None:
        stream_info = StreamInfo(
            extension=extension_hint,
            mimetype=mime_type_hint,
            charset=charset_hint,
        )

    if args.list_plugins:
        print("Installed MarkItDown 3rd-party Plugins:\n")
        plugin_entry_points = list(entry_points(group="markitdown.plugin"))
        if len(plugin_entry_points) == 0:
            print("  * No 3rd-party plugins installed.")
            print("\nFind plugins by searching for the hashtag #markitdown-plugin on GitHub.\n")
        else:
            for entry_point in plugin_entry_points:
                print(f"  * {entry_point.name:<16}\t(package: {entry_point.value})")
            print("\nUse the -p (or --use-plugins) option to enable 3rd-party plugins.\n")
        sys.exit(0)

    if args.use_docintel:
        if args.endpoint is None:
            _exit_with_error(
                "Document Intelligence Endpoint is required when using Document Intelligence."
            )
        elif args.filename is None:
            _exit_with_error("Filename is required when using Document Intelligence.")
        markitdown = MarkItDown(enable_plugins=args.use_plugins, docintel_endpoint=args.endpoint)
    else:
        markitdown = MarkItDown(enable_plugins=args.use_plugins)

    if args.filename is None:
        result = markitdown.convert_stream(
            sys.stdin.buffer,
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        )
    else:
        result = markitdown.convert(
            args.filename,
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        )

    _write_attachments(args.filename, result)
    _handle_output(args, result)


if __name__ == "__main__":
    main()

