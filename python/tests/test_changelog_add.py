"""Тесты scripts/changelog_add.py (работают только с копиями в tmp_path)."""
import importlib.util
from pathlib import Path

import pytest

_PATH = Path(__file__).resolve().parents[2] / "scripts" / "changelog_add.py"
_spec = importlib.util.spec_from_file_location("changelog_add", _PATH)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

SKELETON = """# История

Пишите под `## Unreleased` в раздел `### Changed`.

## Unreleased

### Added

### Changed
- старая запись
  продолжение старой записи
- вторая запись

### Fixed

### Removed

## v1.0.0 — 2020-01-01

### Added
- релизная запись

### Changed
- релизная правка
"""


def _make(tmp_path, text=SKELETON):
    f = tmp_path / "CHANGELOG.md"
    f.write_bytes(text.encode("utf-8"))
    return f


def _run(f, section, text, *extra):
    return mod.main([section, text, "--file", str(f), *extra])


def test_empty_section(tmp_path, capsys):
    f = _make(tmp_path)
    assert _run(f, "Added", "новая") == 0
    assert "+- новая" in capsys.readouterr().out
    lines = f.read_text(encoding="utf-8").splitlines()
    i = lines.index("### Added")
    assert lines[i + 1] == "- новая"
    assert lines[i + 2] == ""


def test_after_multiline_bullets(tmp_path):
    f = _make(tmp_path)
    assert _run(f, "Changed", "- с дефисом") == 0
    lines = f.read_text(encoding="utf-8").splitlines()
    i = lines.index("- вторая запись")
    assert lines[i + 1] == "- с дефисом"
    assert lines[i + 2] == ""
    assert lines[lines.index("- старая запись") + 1] == "  продолжение старой записи"


def test_header_substrings_ignored(tmp_path):
    f = _make(tmp_path)
    assert _run(f, "Changed", "x") == 0
    text = f.read_text(encoding="utf-8")
    head = text.split("\n## Unreleased\n")[0]
    assert "- x" not in head
    assert "Пишите под `## Unreleased` в раздел `### Changed`." in head


def test_never_in_released(tmp_path):
    f = _make(tmp_path)
    for s in ("Added", "Changed", "Fixed", "Removed"):
        assert _run(f, s, "e-" + s) == 0
    text = f.read_text(encoding="utf-8")
    released = text.split("## v1.0.0")[1]
    assert "e-" not in released


def test_no_trailing_newline_preserved(tmp_path):
    f = _make(tmp_path, "## Unreleased\n\n### Added\n- a")
    assert _run(f, "Added", "b") == 0
    assert f.read_text(encoding="utf-8") == "## Unreleased\n\n### Added\n- a\n- b"


@pytest.mark.parametrize("text", [
    "# H\n\n### Added\n",                                           # нет Unreleased
    "## Unreleased\n### Added\n## Unreleased\n### Added\n",    # дубликат
    "## Unreleased\n\n### Changed\n\n## v1.0\n\n### Added\n",   # нет раздела в Unreleased
])
def test_errors_leave_file_unchanged(tmp_path, text):
    f = _make(tmp_path, text)
    assert _run(f, "Added", "z") == 1
    assert f.read_text(encoding="utf-8") == text


def test_dry_run(tmp_path, capsys):
    f = _make(tmp_path)
    assert _run(f, "Fixed", "d", "--dry-run") == 0
    assert f.read_text(encoding="utf-8") == SKELETON
    assert "+- d" in capsys.readouterr().out
