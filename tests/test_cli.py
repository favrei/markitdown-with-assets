import sys
from types import SimpleNamespace
from pathlib import Path

import markitdown_ext.cli as cli


def test_cli_saves_assets(tmp_path, monkeypatch):
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")
    output_md = tmp_path / "out.md"

    attachments = {"file1.txt": b"hello", "image.png": b"\x89PNG\r\n"}

    class FakeResult:
        def __init__(self):
            self.attachments = attachments

    class FakeMarkItDown:
        def convert(self, input_pdf, output_md_path):
            assert Path(input_pdf) == pdf
            Path(output_md_path).write_text("dummy")
            return FakeResult()

    monkeypatch.setitem(sys.modules, "markitdown", SimpleNamespace(MarkItDown=FakeMarkItDown))

    cli.main([str(pdf), str(output_md)])

    assets_dir = tmp_path / "out_assets"
    assert assets_dir.is_dir()
    for name, data in attachments.items():
        assert (assets_dir / name).read_bytes() == data
    assert output_md.is_file()
