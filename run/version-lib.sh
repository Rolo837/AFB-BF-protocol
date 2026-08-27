#!/bin/bash
# Shared helpers for AFB-BF-protocol version scripts. Source from other run/*.sh.
# Expects SCRIPT_DIR to be set to the run/ directory before sourcing.
#
# Родственные файлы в AFB/run и BF/run; здесь адаптированы под раскладку
# протокола (VERSION в корне, версия дублируется в 4 местах).

set -euo pipefail

: "${SCRIPT_DIR:?SCRIPT_DIR must be set before sourcing version-lib.sh}"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION_FILE="$PROJECT_ROOT/VERSION"
CHANGELOG_FILE="$PROJECT_ROOT/CHANGELOG.md"

# Четыре места, где semver-версия обязана совпадать с VERSION.
PYPROJECT_TOML="$PROJECT_ROOT/python/pyproject.toml"
VERSION_PY="$PROJECT_ROOT/python/afb_bf_protocol/version.py"
ASYNCAPI_YAML="$PROJECT_ROOT/spec/asyncapi.yaml"
PACKAGE_JSON="$PROJECT_ROOT/package.json"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

semver_re='^[0-9]+\.[0-9]+\.[0-9]+$'

read_version() {
    if [ ! -f "$VERSION_FILE" ]; then
        echo -e "${RED}Ошибка: не найден $VERSION_FILE${NC}" >&2
        exit 1
    fi
    local v
    v="$(tr -d '[:space:]' < "$VERSION_FILE")"
    if [[ ! "$v" =~ $semver_re ]]; then
        echo -e "${RED}Ошибка: некорректный semver в $VERSION_FILE: '$v'${NC}" >&2
        exit 1
    fi
    printf '%s' "$v"
}

bump_semver() {
    local current="$1"
    local level="$2"
    local major minor patch
    IFS=. read -r major minor patch <<<"$current"
    case "$level" in
        patch) patch=$((patch + 1)) ;;
        minor) minor=$((minor + 1)); patch=0 ;;
        *)
            echo -e "${RED}Ошибка: неизвестный уровень bump: $level${NC}" >&2
            exit 1
            ;;
    esac
    printf '%s.%s.%s' "$major" "$minor" "$patch"
}

require_clean_git() {
    if [ -n "$(git -C "$PROJECT_ROOT" status --porcelain 2>/dev/null)" ]; then
        echo -e "${RED}Ошибка: есть несохранённые изменения. Закоммитьте или спрячьте их.${NC}" >&2
        exit 1
    fi
}

require_branch() {
    local expected="$1"
    local current
    current="$(git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [ "$current" != "$expected" ]; then
        echo -e "${RED}Ошибка: нужна ветка ${expected} (сейчас: ${current:-не в git})${NC}" >&2
        exit 1
    fi
}

# Оформить накопленную секцию "## Unreleased" под версию релиза: вставляет
# "## vX.Y.Z — YYYY-MM-DD" сразу под строкой Unreleased, сама Unreleased остаётся
# сверху пустой. Записи в CHANGELOG.md ведёт разработчик/ассистент по ходу работы,
# без версии — см. VERSIONING.md. no-op, если файла/секции нет.
stamp_changelog() {
    local version="$1"
    [ -f "$CHANGELOG_FILE" ] || return 0
    python3 - "$CHANGELOG_FILE" "$version" "$(date +%Y-%m-%d)" <<'PY'
import pathlib, re, sys
path, version, date_str = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
out, done = [], False
for line in lines:
    out.append(line)
    if not done and re.match(r'(?i)^##\s*\[?unreleased\]?\s*$', line):
        nl = "\n" if line.endswith("\n") else ""
        out.append(nl)
        out.append(f"## v{version} — {date_str}{nl}")
        done = True
if done:
    path.write_text("".join(out), encoding="utf-8")
    print(f"CHANGELOG: секция Unreleased оформлена как v{version} — {date_str}")
else:
    print("CHANGELOG: секция ## Unreleased не найдена — пропуск", file=sys.stderr)
PY
}

# --- чтение версии из каждого источника (для check-version.sh) --------------

read_pyproject_version() {
    python3 -c "import re,pathlib; t=pathlib.Path(r'$PYPROJECT_TOML').read_text(); m=re.search(r'(?m)^version\s*=\s*\"([^\"]+)\"', t); print(m.group(1) if m else '')"
}

read_version_py() {
    python3 -c "import re,pathlib; t=pathlib.Path(r'$VERSION_PY').read_text(); m=re.search(r'__version__\s*=\s*\"([^\"]+)\"', t); print(m.group(1) if m else '')"
}

read_asyncapi_version() {
    python3 -c "import re,pathlib; t=pathlib.Path(r'$ASYNCAPI_YAML').read_text(); m=re.search(r'(?m)^\s+version:\s*([0-9][^\s#]*)', t); print(m.group(1) if m else '')"
}

read_package_json_version() {
    python3 -c "import json,pathlib; print(json.loads(pathlib.Path(r'$PACKAGE_JSON').read_text()).get('version',''))"
}

# --- запись версии во все 4 места (для version.sh) -------------------------

write_version_files() {
    local new_version="$1"
    printf '%s\n' "$new_version" > "$VERSION_FILE"

    python3 - "$PYPROJECT_TOML" "$new_version" <<'PY'
import pathlib, re, sys
path, version = pathlib.Path(sys.argv[1]), sys.argv[2]
text = path.read_text(encoding="utf-8")
text2, n = re.subn(r'(?m)^(version\s*=\s*")[^"]+(")', rf'\g<1>{version}\g<2>', text, count=1)
if n != 1:
    raise SystemExit(f"не удалось обновить version в {path}")
path.write_text(text2, encoding="utf-8")
PY

    python3 - "$VERSION_PY" "$new_version" <<'PY'
import pathlib, re, sys
path, version = pathlib.Path(sys.argv[1]), sys.argv[2]
text = path.read_text(encoding="utf-8")
text2, n = re.subn(r'(__version__\s*=\s*")[^"]+(")', rf'\g<1>{version}\g<2>', text, count=1)
if n != 1:
    raise SystemExit(f"не удалось обновить __version__ в {path}")
path.write_text(text2, encoding="utf-8")
PY

    python3 - "$ASYNCAPI_YAML" "$new_version" <<'PY'
import pathlib, re, sys
path, version = pathlib.Path(sys.argv[1]), sys.argv[2]
text = path.read_text(encoding="utf-8")
# info.version — первое поле "  version:" в файле (внутри info:)
text2, n = re.subn(r'(?m)^(\s+version:\s*)[0-9][^\s#]*', rf'\g<1>{version}', text, count=1)
if n != 1:
    raise SystemExit(f"не удалось обновить info.version в {path}")
path.write_text(text2, encoding="utf-8")
PY

    python3 - "$PACKAGE_JSON" "$new_version" <<'PY'
import json, pathlib, sys
path, version = pathlib.Path(sys.argv[1]), sys.argv[2]
data = json.loads(path.read_text(encoding="utf-8"))
data["version"] = version
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY
}
