# Test suite for markitdown_ext CLI asset extraction

import os
from pathlib import Path
import sys
import types

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

dummy_markitdown = types.ModuleType("markitdown")
dummy_markitdown.__about__ = types.SimpleNamespace(__version__="0.0")
dummy_markitdown._markitdown = types.SimpleNamespace(
    MarkItDown=object, StreamInfo=object, DocumentConverterResult=object
)
sys.modules.setdefault("markitdown", dummy_markitdown)
sys.modules.setdefault("markitdown.__about__", dummy_markitdown.__about__)
sys.modules.setdefault("markitdown._markitdown", dummy_markitdown._markitdown)

import pytest

# Import the CLI entrypoint
from markitdown_ext.cli import main

def test_asset_extraction_creates_assets(tmp_path, monkeypatch):
    """Test that running the CLI on 1706.03762v7.pdf creates an assets directory and rewrites links."""
    # Arrange
    pdf_path = Path(__file__).parent / "fixtures" / "1706.03762v7.pdf"
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    output_file = output_dir / "result.md"
    # Assets directory is now based on the output file's stem and location
    assets_dir = output_file.parent / (output_file.stem + "_assets")

    class DummyResult:
        def __init__(self) -> None:
            self.markdown = "![img](image.png)"
            self.attachments = {"image.png": b"binarydata"}

    class DummyMarkItDown:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def convert(self, *args, **kwargs):
            return DummyResult()

    monkeypatch.setattr("markitdown_ext.cli.MarkItDown", DummyMarkItDown)

    # Run main directly without changing CWD
    main([str(pdf_path), "-o", str(output_file)])

    asset_file = assets_dir / "image.png"
    assert asset_file.is_file()
    assert asset_file.read_bytes() == b"binarydata"
    # The markdown should reference the path to the asset relative to the markdown file.
    # assets_dir.name will be "result_assets"
    assert f"{assets_dir.name}/image.png" in output_file.read_text()
