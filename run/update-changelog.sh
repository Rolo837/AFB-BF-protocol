#!/bin/bash
# Черновик секции CHANGELOG.md из git log с предыдущего semver-тега.
# Не перезаписывает CHANGELOG молча: пишет CHANGELOG.md.draft и требует ручной правки.
#
# Использование:
#   ./run/update-changelog.sh              # черновик для VERSION из корневого VERSION
#   ./run/update-changelog.sh 2.6.0        # черновик для указанной версии
#   ./run/update-changelog.sh --extract 2.5.16 > /tmp/notes.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/version-lib.sh"

usage() {
    echo "Использование:"
    echo "  ./run/update-changelog.sh [X.Y.Z]          # создать CHANGELOG.md.draft"
    echo "  ./run/update-changelog.sh --extract X.Y.Z  # печатать notes секции в stdout"
}

if [ "${1:-}" = "--extract" ]; then
    if [ -z "${2:-}" ]; then usage; exit 1; fi
    tmp="$(mktemp)"
    extract_changelog_notes "$2" "$tmp"
    cat "$tmp"
    rm -f "$tmp"
    exit 0
fi

if [ -n "${1:-}" ]; then
    VERSION="$1"
    if [[ ! "$VERSION" =~ $semver_re ]]; then
        echo -e "${RED}Ошибка: ожидается semver X.Y.Z${NC}" >&2
        exit 1
    fi
else
    VERSION="$(read_version)"
fi

cd "$PROJECT_ROOT"

if [ ! -f "$CHANGELOG_FILE" ]; then
    echo -e "${RED}Ошибка: не найден $CHANGELOG_FILE${NC}" >&2
    exit 1
fi

if changelog_has_version "$VERSION"; then
    echo -e "${YELLOW}Секция для ${VERSION} уже есть в CHANGELOG.md — черновик не создан.${NC}"
    exit 0
fi

prev_tag=""
for t in $(git tag -l 'v*' 2>/dev/null | sort -V); do
    ver="${t#v}"
    [[ "$ver" =~ $semver_re ]] || continue
    if [ "$ver" != "$VERSION" ] && [ "$(printf '%s\n%s\n' "$ver" "$VERSION" | sort -V | head -1)" = "$ver" ]; then
        prev_tag="$t"
    fi
done

if [ -z "$prev_tag" ]; then
    rev_range="HEAD"
else
    rev_range="${prev_tag}..HEAD"
fi

date_str="$(date +%Y-%m-%d)"
draft="$CHANGELOG_FILE.draft"

{
    echo "## v${VERSION} — ${date_str}"
    echo ""
    echo "PATCH|MINOR. <краткое резюме; почему именно этот уровень — см. VERSIONING.md §2>"
    echo ""
    echo "<!-- Черновик коммитов из ${rev_range}; перепишите по существу и удалите этот блок. -->"
    git log "$rev_range" --format='%s' --no-merges 2>/dev/null | while read -r line; do
        [ -z "$line" ] && continue
        case "$line" in
            [Bb]ump\ version*|[Cc]hore:\ bump*|release\ v*|Обновление\ версии*) continue ;;
        esac
        echo "- ${line}"
    done
    echo ""
    echo "- **Версии**: bump до \`${VERSION}\` в \`VERSION\`, \`package.json\`, \`python/pyproject.toml\`, \`python/afb_bf_protocol/version.py\`, \`spec/asyncapi.yaml\`."
    echo ""
} > "$draft"

echo -e "${GREEN}Черновик:${NC} $draft"
echo "1) Перепишите резюме и пункты по существу"
echo "2) Вставьте блок в начало $CHANGELOG_FILE (перед первой ## v..)"
echo "3) Удалите $draft"
