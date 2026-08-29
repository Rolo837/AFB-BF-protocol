#!/bin/bash
# Ручной bump semver-версии протокола. Не коммитит, не тегирует, не пушит.
# Пишет во все 4 синхронных места + корневой VERSION.
#
# Использование:
#   ./run/version.sh patch
#   ./run/version.sh minor
#   ./run/version.sh set 2.6.0
#   ./run/version.sh show
#
# MAJOR через set запрещён политикой протокола (VERSIONING.md §2) — скрипт не
# запрещает механически, но поднимать первую цифру можно только по явной команде.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/version-lib.sh"

usage() {
    echo "Использование: ./run/version.sh {patch|minor|set X.Y.Z|show}"
    echo "  patch  — X.Y.Z → X.Y.(Z+1)"
    echo "  minor  — X.Y.Z → X.(Y+1).0"
    echo "  set    — установить явную версию"
    echo "  show   — показать текущую версию и статус синхрона"
}

cmd="${1:-show}"
case "$cmd" in
    show)
        current="$(read_version)"
        echo "VERSION:                       $current"
        echo "python/pyproject.toml:         $(read_pyproject_version)"
        echo "python/.../version.py:         $(read_version_py)"
        echo "spec/asyncapi.yaml info:       $(read_asyncapi_version)"
        echo "package.json:                  $(read_package_json_version)"
        "$SCRIPT_DIR/check-version.sh"
        ;;
    patch|minor)
        current="$(read_version)"
        new_version="$(bump_semver "$current" "$cmd")"
        echo -e "Версия: ${YELLOW}${current}${NC} → ${GREEN}${new_version}${NC} ($cmd)"
        write_version_files "$new_version"
        stamp_changelog "$new_version"
        echo -e "${GREEN}Обновлены VERSION + pyproject.toml + version.py + asyncapi.yaml + package.json${NC}"
        echo "Дальше: commit + ./run/release.sh tag [--afb] [--bf]."
        ;;
    set)
        new_version="${2:-}"
        if [[ ! "$new_version" =~ $semver_re ]]; then
            echo -e "${RED}Ошибка: ожидается semver X.Y.Z${NC}" >&2
            usage
            exit 1
        fi
        current="$(read_version)"
        echo -e "Версия: ${YELLOW}${current}${NC} → ${GREEN}${new_version}${NC} (set)"
        write_version_files "$new_version"
        stamp_changelog "$new_version"
        echo -e "${GREEN}Обновлены VERSION + pyproject.toml + version.py + asyncapi.yaml + package.json${NC}"
        echo "Дальше: commit + ./run/release.sh tag [--afb] [--bf]."
        ;;
    -h|--help)
        usage
        ;;
    *)
        echo -e "${RED}Неизвестная команда: $cmd${NC}" >&2
        usage
        exit 1
        ;;
esac
