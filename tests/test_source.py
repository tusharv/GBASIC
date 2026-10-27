import subprocess
import sys

import pytest
from textual.widgets import TextArea

from ghost_basic.devices import Disk
from ghost_basic.errors import BasicError
from ghost_basic.source import decode_source
from ghost_basic.tui import GhostBasicApp


@pytest.mark.parametrize(
    "data, expected",
    [
        (b'10 PRINT "Hello"\r\n', '10 PRINT "Hello"\n'),
        ('10 PRINT "café"\n'.encode("utf-8"), '10 PRINT "café"\n'),
        (b"\xef\xbb\xbf10 END\r\n", "10 END\n"),
        (b'10 PRINT "\xda\xc4\xbf"\r\n', '10 PRINT "┌─┐"\n'),
        (b"10 END\r\n\x1a", "10 END\n"),
    ],
)
def test_decode_legacy_and_utf8(data, expected):
    assert decode_source(data) == expected


@pytest.mark.parametrize("data", [b"\xff\x01\x02", b"\xfe\x01\x02", b"10 \x00END"])
def test_reject_binary_formats(data):
    with pytest.raises(BasicError, match="not supported"):
        decode_source(data)


def test_disk_reads_cp437_and_saves_utf8(tmp_path):
    path = tmp_path / "dos.bas"
    path.write_bytes(b'10 PRINT "\xda\xc4\xbf"\r\n\x1a')
    disk = Disk(tmp_path)
    source = disk.read("dos.bas")
    assert "┌─┐" in source
    disk.write("converted.bas", source)
    assert (tmp_path / "converted.bas").read_text(encoding="utf-8") == source
    assert path.read_bytes() == b'10 PRINT "\xda\xc4\xbf"\r\n\x1a'


def test_batch_reads_cp437(tmp_path):
    path = tmp_path / "dos.bas"
    path.write_bytes(b'10 PRINT "\xda\xc4\xbf"\r\n\x1a')
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic", str(path)],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "┌─┐\n"


@pytest.mark.asyncio
async def test_editor_opens_unnumbered_dos_qbasic(tmp_path):
    (tmp_path / "money.bas").write_bytes(
        b'\' Money\r\nDECLARE SUB Box ()\r\nPRINT "\xda\xc4\xbf"\r\n'
    )
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        app.open_file("money.bas")
        assert "┌─┐" in app.query_one("#editor", TextArea).text
        assert not app.dirty
        await pilot.press("f5")
        for _ in range(100):
            await pilot.pause(0.02)
            if not app.runner.running:
                app.poll_execution()
                break
        assert "Unnumbered QBasic" in app.output_text
        assert "not supported" in app.output_text
