#!/bin/bash
# Git-тег версии и стабильный GitHub Release для AFB-BF-protocol.
#
# Обычно вызывается из единого релизного комплекса AFB (AFB/run/release.sh),
# но работает и самостоятельно.
#
# Использование:
#   ./run/release.sh tag       # аннотированный vX.Y.Z на develop (после bump версии)
#   ./run/release.sh publish   # merge develop→main + GitHub Release на существующем теге
#   ./run/release.sh tag --dry-run
#   ./run/release.sh publish --dry-run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/version-lib.sh"

DRY_RUN=false
COMMAND=""

usage() {
    echo "Использование: ./run/release.sh {tag|publish} [--dry-run]"
    echo "  tag:     git tag vVERSION на текущем commit develop + push тега"
    echo "  publish: PR/merge develop→main (develop не удаляется) + GitHub Release"
}

for arg in "$@"; do
    case "$arg" in
        tag|publish)
            if [ -n "$COMMAND" ]; then
                echo -e "${RED}Ошибка: укажите одну команду${NC}" >&2
                usage
                exit 1
            fi
            COMMAND="$arg"
            ;;
        --dry-run) DRY_RUN=true ;;
        -h|--help) usage; exit 0 ;;
        *)
            echo -e "${RED}Неизвестный аргумент: $arg${NC}" >&2
            usage
            exit 1
            ;;
    esac
done

if [ -z "$COMMAND" ]; then
    usage
    exit 1
fi

VERSION="$(read_version)"
TAG="v${VERSION}"
cd "$PROJECT_ROOT"

run_or_echo() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[dry-run] $*${NC}"
    else
        "$@"
    fi
}

preflight_common() {
    require_branch "develop"
    "$SCRIPT_DIR/check-version.sh"
    if ! command -v gh >/dev/null 2>&1; then
        echo -e "${RED}Ошибка: нужен GitHub CLI (gh). https://cli.github.com/${NC}" >&2
        exit 1
    fi
}

do_tag() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Git tag ${TAG} (protocol)${NC}"
    echo -e "${GREEN}========================================${NC}"
    preflight_common

    if git rev-parse "$TAG" >/dev/null 2>&1; then
        echo -e "${RED}Ошибка: тег ${TAG} уже существует локально${NC}" >&2
        exit 1
    fi
    if git ls-remote --tags origin "refs/tags/${TAG}" 2>/dev/null | grep -q "$TAG"; then
        echo -e "${RED}Ошибка: тег ${TAG} уже есть на origin${NC}" >&2
        exit 1
    fi

    echo -e "${YELLOW}Пуш develop на origin...${NC}"
    run_or_echo git push origin develop

    echo -e "${YELLOW}Создание аннотированного тега ${TAG}...${NC}"
    run_or_echo git tag -a "$TAG" -m "Version ${VERSION}"
    run_or_echo git push origin "$TAG"

    echo -e "${GREEN}Тег ${TAG} создан на develop. Merge в main — ./run/release.sh publish${NC}"
}

do_publish() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Release publish ${TAG} (protocol)${NC}"
    echo -e "${GREEN}========================================${NC}"
    preflight_common

    if ! git rev-parse "$TAG" >/dev/null 2>&1; then
        echo -e "${RED}Ошибка: локального тега ${TAG} нет. Сначала ./run/release.sh tag${NC}" >&2
        exit 1
    fi

    echo -e "${YELLOW}Пуш develop на origin...${NC}"
    run_or_echo git push origin develop

    echo -e "${YELLOW}PR develop → main...${NC}"
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[dry-run] gh pr create/merge develop→main${NC}"
    else
        if ! gh pr view develop --base main >/dev/null 2>&1; then
            gh pr create --base main --head develop \
                --title "Release v${VERSION}" \
                --body "Release v${VERSION}"
        else
            echo -e "${YELLOW}PR develop→main уже существует — используем его${NC}"
        fi
        gh pr merge develop --merge --delete-branch=false
    fi

    echo -e "${YELLOW}Обновление main...${NC}"
    run_or_echo git fetch origin main

    if [ "$DRY_RUN" = false ]; then
        if ! git merge-base --is-ancestor "$TAG" origin/main; then
            echo -e "${YELLOW}Предупреждение: тег ${TAG} не является предком origin/main после merge.${NC}"
        fi
    fi

    echo -e "${YELLOW}GitHub Release ${TAG}...${NC}"
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[dry-run] gh release create ${TAG} --generate-notes${NC}"
    else
        if gh release view "$TAG" >/dev/null 2>&1; then
            echo -e "${YELLOW}GitHub Release ${TAG} уже существует — пропуск${NC}"
        else
            gh release create "$TAG" \
                --title "Версия ${VERSION}" \
                --generate-notes
        fi
    fi

    echo -e "${YELLOW}Синхронизация develop с main...${NC}"
    run_or_echo git fetch origin main
    run_or_echo git merge origin/main -m "Merge main after release v${VERSION}"
    run_or_echo git push origin develop

    echo -e "${GREEN}Release v${VERSION} протокола опубликован (ветка develop сохранена)${NC}"
}

case "$COMMAND" in
    tag) do_tag ;;
    publish) do_publish ;;
esac
