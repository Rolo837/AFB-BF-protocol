#!/usr/bin/env python3
"""Добавление записи в секцию Unreleased файла CHANGELOG.md.

Единственный разрешённый способ дописывать записи в CHANGELOG.md.
Файл одинаков во всех репозиториях, отличается только блок настройки ниже.

Использование:
    skeleton / on-demand:
        python3 scripts/changelog_add.py <Added|Changed|Fixed|Removed> "текст" [--file PATH] [--dry-run]
    flat:
        python3 scripts/changelog_add.py "текст" [--file PATH] [--dry-run]

Работает со списком строк: границы Unreleased определяются по строке, ТОЧНО равной
UNRELEASED_HEADING (а не по подстроке), конец — первая следующая строка, начинающаяся с `## `.
Вне диапазона Unreleased ничего не меняется. При ошибке — код 1 и файл не тронут.

SECTIONS_MODE:
    skeleton  — подраздел `### X` обязан существовать в Unreleased, иначе ошибка;
    on-demand — отсутствующий подраздел создаётся в Unreleased в порядке Added, Changed, Fixed, Removed;
    flat      — подразделов нет, запись добавляется после последнего маркера под заголовком Unreleased.
"""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

# ---- настройка репозитория (единственное отличие файла между репозиториями) ----
UNRELEASED_HEADING = "## Unreleased"
SECTIONS_MODE = "skeleton"  # 'skeleton' | 'on-demand' | 'flat'
# --------------------------------------------------------------------------------

SECTIONS = ("Added", "Changed", "Fixed", "Removed")
DEFAULT_FILE = Path(__file__).resolve().parent.parent / "CHANGELOG.md"


class ChangelogError(Exception):
    pass


def normalize_entry(text: str) -> str:
    """Приводит текст к одной строке вида `- текст`."""
    one = " ".join(text.split())
    if one.startswith("- "):
        one = one[2:].lstrip()
    elif one == "-":
        one = ""
    if not one:
        raise ChangelogError("пустой текст записи")
    return "- " + one


def _is_blank(ln: str) -> bool:
    return not ln.strip()


def _bounds(lines: list[str]) -> tuple[int, int]:
    starts = [i for i, ln in enumerate(lines) if ln.rstrip("\r\n") == UNRELEASED_HEADING]
    if len(starts) != 1:
        raise ChangelogError(
            f"строка «{UNRELEASED_HEADING}» должна встречаться ровно один раз, найдено: {len(starts)}"
        )
    start = starts[0]
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def _last_bullet(lines: list[str], head: int, end: int) -> int:
    """Индекс последней строки блока маркеров сразу после строки head (или head, если маркеров нет).

    Берутся подряд идущие `- ` строки и их продолжения (отступ из двух пробелов).
    """
    pos = head + 1
    last = head
    while pos < end:
        ln = lines[pos]
        if ln.startswith("- ") or (last != head and ln.startswith("  ")):
            last = pos
            pos += 1
        else:
            break
    return last


def _insert_after(lines: list[str], last: int, entry: str) -> list[str]:
    result = list(lines)
    new_line = entry + "\n"
    # Вставка после последней строки файла без перевода строки.
    if result[last] and not result[last].endswith("\n"):
        result[last] = result[last] + "\n"
        new_line = entry  # сохраняем отсутствие финального перевода строки
    result.insert(last + 1, new_line)
    return result


def _create_section(lines: list[str], start: int, end: int, section: str, entry: str) -> list[str]:
    idx = SECTIONS.index(section)
    nxt = None  # первый по порядку файла подраздел с большим каноническим номером
    for i in range(start + 1, end):
        name = lines[i].rstrip("\r\n")
        if name.startswith("### ") and name[4:] in SECTIONS and SECTIONS.index(name[4:]) > idx:
            nxt = i
            break
    result = list(lines)
    if nxt is not None:
        result[nxt:nxt] = [f"### {section}\n", entry + "\n", "\n"]
        return result
    # В конец Unreleased: после последней непустой строки диапазона.
    last = start
    for i in range(start + 1, end):
        if not _is_blank(lines[i]):
            last = i
    if not result[last].endswith("\n"):
        result[last] += "\n"
    block = ["\n", f"### {section}\n", entry + "\n"]
    if last + 1 < len(lines) and not _is_blank(lines[last + 1]):
        block.append("\n")
    result[last + 1:last + 1] = block
    return result


def insert_entry(lines: list[str], section: str | None, entry: str) -> list[str]:
    """Возвращает новый список строк со вставленной записью."""
    start, end = _bounds(lines)

    if SECTIONS_MODE == "flat":
        p = start + 1
        while p < end and _is_blank(lines[p]):
            p += 1
        last = start
        if p < end and lines[p].startswith("- "):
            last = _last_bullet(lines, p - 1, end)
        if last != start:
            return _insert_after(lines, last, entry)
        result = list(lines)
        q = start + 1
        if q < len(result) and _is_blank(result[q]):
            q += 1
            add = []
        else:
            add = ["\n"]
        if result[start] and not result[start].endswith("\n"):
            result[start] += "\n"
        add.append(entry + "\n")
        if q < len(result) and not _is_blank(result[q]):
            add.append("\n")
        result[q:q] = add
        return result

    heading = f"### {section}"
    hpos = None
    for i in range(start + 1, end):
        if lines[i].rstrip("\r\n") == heading:
            hpos = i
            break
    if hpos is None:
        if SECTIONS_MODE == "on-demand":
            return _create_section(lines, start, end, section, entry)
        raise ChangelogError(f"в Unreleased нет подраздела «{heading}»")
    return _insert_after(lines, _last_bullet(lines, hpos, end), entry)


def run(section: str | None, text: str, path: Path, dry_run: bool) -> int:
    try:
        entry = normalize_entry(text)
        raw = path.read_bytes().decode("utf-8")
        old = raw.splitlines(keepends=True)
        new = insert_entry(old, section, entry)
    except ChangelogError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Ошибка чтения {path}: {e}", file=sys.stderr)
        return 1

    diff = "".join(difflib.unified_diff(old, new, f"{path} (было)", f"{path} (стало)"))
    if not dry_run:
        path.write_bytes("".join(new).encode("utf-8"))
    sys.stdout.write(diff if diff.endswith("\n") else diff + "\n")
    if dry_run:
        print("(dry-run: файл не изменён)")
    return 0


def main(argv: list[str] | None = None) -> int:
    if SECTIONS_MODE not in ("skeleton", "on-demand", "flat"):
        print(f"Ошибка: неизвестный SECTIONS_MODE «{SECTIONS_MODE}»", file=sys.stderr)
        return 1
    p = argparse.ArgumentParser(description="Добавить запись в секцию Unreleased CHANGELOG.md")
    if SECTIONS_MODE != "flat":
        p.add_argument("section", choices=SECTIONS, help="подраздел")
    p.add_argument("text", help="текст записи")
    p.add_argument("--file", default=str(DEFAULT_FILE), help="путь к CHANGELOG.md")
    p.add_argument("--dry-run", action="store_true", help="только показать diff")
    a = p.parse_args(argv)
    return run(getattr(a, "section", None), a.text, Path(a.file), a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
