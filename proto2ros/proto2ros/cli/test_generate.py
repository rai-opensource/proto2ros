# Copyright (c) 2025 Robotics and AI Institute LLC dba RAI Institute. All rights reserved.

"""Unit tests for proto2ros.cli.generate."""

import pathlib

from proto2ros.cli.generate import write_text_if_changed


def test_write_text_if_changed_creates_file(tmp_path: pathlib.Path) -> None:
    """A missing file is created with the requested content."""
    target = tmp_path / "out.txt"
    write_text_if_changed(target, "hello\n")
    assert target.read_text() == "hello\n"


def test_write_text_if_changed_is_noop_when_unchanged(tmp_path: pathlib.Path) -> None:
    """Rewriting identical content must not touch the file (stable mtime).

    Generated files are both build outputs and CMake configure-time
    dependencies; bumping their mtime on every generation causes an endless
    CMake/Ninja reconfigure loop. This guards that regression.
    """
    target = tmp_path / "out.txt"
    target.write_text("same\n")
    before_ns = target.stat().st_mtime_ns

    write_text_if_changed(target, "same\n")

    assert target.read_text() == "same\n"
    assert target.stat().st_mtime_ns == before_ns, "unchanged content must not rewrite the file"


def test_write_text_if_changed_updates_on_difference(tmp_path: pathlib.Path) -> None:
    """Differing content is written out."""
    target = tmp_path / "out.txt"
    target.write_text("old\n")

    write_text_if_changed(target, "new\n")

    assert target.read_text() == "new\n"
