# Test suite for markitdown_ext CLI asset extraction

import pytest
from pathlib import Path

# Import the CLI entrypoint
from markitdown_ext.cli import main

def test_asset_extraction_creates_assets(tmp_path):
    """Test that running the CLI on 1706.03762v7.pdf creates an assets directory and rewrites links."""
    # Arrange
    pdf_path = Path(__file__).parent / "fixtures" / "1706.03762v7.pdf"
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    assets_dir = output_dir / f"{pdf_path.stem}_assets"

    # TODO: invoke the CLI and assert assets_dir exists with correct files
    pytest.skip("Not implemented yet") 