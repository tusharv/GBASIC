from ghost_basic.devices import Disk


def test_examples_sorted_filtered_and_confined(tmp_path):
    folder = tmp_path / "examples"
    folder.mkdir()
    (folder / "z.bas").write_text("10 END")
    (folder / "A.BAS").write_text("10 END")
    (folder / "readme.txt").write_text("text")
    (folder / "directory.bas").mkdir()
    outside = tmp_path.parent / "outside-picker.bas"
    outside.write_text("10 END")
    (folder / "escape.bas").symlink_to(outside)
    assert Disk(tmp_path).example_programs() == ("examples/A.BAS", "examples/z.bas")


def test_missing_or_external_examples_folder(tmp_path):
    assert Disk(tmp_path).example_programs() == ()
    (tmp_path / "examples").symlink_to(tmp_path.parent, target_is_directory=True)
    assert Disk(tmp_path).example_programs() == ()
