#!/bin/bash
# Релиз AFB-BF-protocol. Не собирает AFB/BF.
#
#   ./run/release.sh tag [--afb] [--bf] [--dry-run]
#   ./run/release.sh publish [--dry-run]
#   ./run/release.sh pin --afb [--bf] [--dry-run]
#
# tag:     аннотированный vX.Y.Z на develop + push тега.
#          При --afb/--bf (по умолчанию выкл.) после успешного тега ставит пин
#          @vX.Y.Z в соседнем AFB и/или BF и коммитит его.
# publish: merge develop→main + GitHub Release (develop не удаляется).
# pin:     только пины потребителей на уже существующий тег текущей VERSION
#          (если tag уже прошёл, а --afb/--bf не передавали).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/version-lib.sh"

DRY_RUN=false
COMMAND=""
PIN_AFB=false
PIN_BF=false

usage() {
    echo "Использование:"
    echo "  ./run/release.sh tag [--afb] [--bf] [--dry-run]"
    echo "  ./run/release.sh publish [--dry-run]"
    echo "  ./run/release.sh pin --afb [--bf] [--dry-run]"
    echo
    echo "  tag:     git tag vVERSION на develop + push тега"
    echo "  publish: PR/merge develop→main (develop не удаляется) + GitHub Release"
    echo "  --afb / --bf: после успешного tag (или команда pin) поставить пин"
    echo "                @vVERSION в AFB и/или BF и закоммитить. По умолчанию нет."
}

while [ $# -gt 0 ]; do
    case "$1" in
        tag|publish|pin)
            [ -n "$COMMAND" ] && { echo -e "${RED}Ошибка: одна команда${NC}" >&2; usage; exit 1; }
            COMMAND="$1" ;;
        --afb) PIN_AFB=true ;;
        --bf) PIN_BF=true ;;
        --dry-run) DRY_RUN=true ;;
        -h|--help) usage; exit 0 ;;
        *)
            echo -e "${RED}Неизвестный аргумент: $1${NC}" >&2
            usage
            exit 1
            ;;
    esac
    shift
done

if [ -z "$COMMAND" ]; then
    usage
    exit 1
fi

VERSION="$(read_version)"
TAG="v${VERSION}"
cd "$PROJECT_ROOT"

AFB_ROOT="$(cd "$PROJECT_ROOT/../AFB" 2>/dev/null && pwd || true)"
BF_ROOT="$(cd "$PROJECT_ROOT/../BF" 2>/dev/null && pwd || true)"

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

require_sibling() {
    local name="$1" root="$2"
    [ -n "$root" ] && [ -d "$root/.git" ] || {
        echo -e "${RED}Ошибка: не найден соседний ${name} (ожидается ../${name})${NC}" >&2
        exit 1
    }
}

require_consumer_ready() {
    local name="$1" root="$2"
    require_sibling "$name" "$root"
    local branch
    branch="$(git -C "$root" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [ "$branch" != "develop" ]; then
        echo -e "${RED}Ошибка: ${name} не на develop (сейчас: ${branch:-?})${NC}" >&2
        exit 1
    fi
    if [ -n "$(git -C "$root" status --porcelain 2>/dev/null)" ]; then
        echo -e "${RED}Ошибка: в ${name} есть несохранённые изменения — сначала закоммить${NC}" >&2
        exit 1
    fi
}

# Пин python-зависимости: git+...@<ref>#subdirectory=python
set_python_pin() {
    local file="$1" ref="$2"
    [ -f "$file" ] || { echo -e "${RED}Нет файла ${file}${NC}" >&2; exit 1; }
    run_or_echo sed -i "s|\(AFB-BF-protocol\.git@\)[^#]*\(#subdirectory=python\)|\1${ref}\2|" "$file"
}

set_afb_pin() {
    local ref="$1"
    require_consumer_ready "AFB" "$AFB_ROOT"
    echo -e "${GREEN}=== Пин AFB → ${ref} ===${NC}"
    set_python_pin "$AFB_ROOT/requirements.txt" "$ref"
    set_python_pin "$AFB_ROOT/informer/requirements.txt" "$ref"
    run_or_echo sed -i "s|\(github:Rolo837/AFB-BF-protocol#\)[^\"]*|\1${ref}|" \
        "$AFB_ROOT/frontend/package.json"
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[dry-run] (cd AFB/frontend && npm install --package-lock-only)${NC}"
    else
        ( cd "$AFB_ROOT/frontend" && npm install --package-lock-only --no-audit --loglevel=error )
    fi
    run_or_echo git -C "$AFB_ROOT" add \
        requirements.txt informer/requirements.txt \
        frontend/package.json frontend/package-lock.json
    if [ "$DRY_RUN" = true ] || [ -n "$(git -C "$AFB_ROOT" diff --cached --name-only)" ]; then
        run_or_echo git -C "$AFB_ROOT" commit -m "chore: pin afb-bf-protocol @${ref}"
        run_or_echo git -C "$AFB_ROOT" push origin develop
    else
        echo -e "${YELLOW}AFB уже на ${ref} — коммит не нужен${NC}"
    fi
}

set_bf_pin() {
    local ref="$1"
    require_consumer_ready "BF" "$BF_ROOT"
    echo -e "${GREEN}=== Пин BF → ${ref} ===${NC}"
    set_python_pin "$BF_ROOT/requirements.txt" "$ref"
    set_python_pin "$BF_ROOT/pyproject.toml" "$ref"
    run_or_echo git -C "$BF_ROOT" add requirements.txt pyproject.toml
    if [ "$DRY_RUN" = true ] || [ -n "$(git -C "$BF_ROOT" diff --cached --name-only)" ]; then
        run_or_echo git -C "$BF_ROOT" commit -m "chore: pin afb-bf-protocol @${ref}"
        run_or_echo git -C "$BF_ROOT" push origin develop
    else
        echo -e "${YELLOW}BF уже на ${ref} — коммит не нужен${NC}"
    fi
}

pin_consumers() {
    if [ "$PIN_AFB" = false ] && [ "$PIN_BF" = false ]; then
        echo -e "${YELLOW}Пины потребителей не трогаем (нет --afb/--bf)${NC}"
        return 0
    fi
    [ "$PIN_AFB" = true ] && set_afb_pin "$TAG"
    [ "$PIN_BF" = true ] && set_bf_pin "$TAG"
}

do_tag() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Git tag ${TAG} (protocol)${NC}"
    echo -e "${GREEN}========================================${NC}"
    preflight_common
    require_clean_git

    if git rev-parse "$TAG" >/dev/null 2>&1; then
        echo -e "${RED}Ошибка: тег ${TAG} уже существует локально${NC}" >&2
        exit 1
    fi
    if git ls-remote --tags origin "refs/tags/${TAG}" 2>/dev/null | grep -q "$TAG"; then
        echo -e "${RED}Ошибка: тег ${TAG} уже есть на origin${NC}" >&2
        exit 1
    fi

    # потребители — до тега, чтобы не оставить тег без возможности отката пина
    [ "$PIN_AFB" = true ] && require_consumer_ready "AFB" "$AFB_ROOT"
    [ "$PIN_BF" = true ] && require_consumer_ready "BF" "$BF_ROOT"

    echo -e "${YELLOW}Пуш develop на origin...${NC}"
    run_or_echo git push origin develop

    echo -e "${YELLOW}Создание аннотированного тега ${TAG}...${NC}"
    run_or_echo git tag -a "$TAG" -m "Version ${VERSION}"
    run_or_echo git push origin "$TAG"

    echo -e "${GREEN}Тег ${TAG} создан на develop.${NC}"
    pin_consumers
    echo -e "${GREEN}Merge в main — ./run/release.sh publish${NC}"
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

do_pin() {
    preflight_common
    if [ "$PIN_AFB" = false ] && [ "$PIN_BF" = false ]; then
        echo -e "${RED}Ошибка: pin требует --afb и/или --bf${NC}" >&2
        exit 1
    fi
    if ! git rev-parse "$TAG" >/dev/null 2>&1 \
       && ! git ls-remote --tags origin "refs/tags/${TAG}" 2>/dev/null | grep -q "$TAG"; then
        echo -e "${RED}Ошибка: тега ${TAG} нет. Сначала ./run/release.sh tag${NC}" >&2
        exit 1
    fi
    pin_consumers
}

case "$COMMAND" in
    tag) do_tag ;;
    publish) do_publish ;;
    pin) do_pin ;;
esac
