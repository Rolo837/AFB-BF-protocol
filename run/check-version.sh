#!/bin/bash
# Проверка синхрона VERSION ↔ 4 источника версии протокола. Read-only.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/version-lib.sh"

expected="$(read_version)"
errors=0

check_eq() {
    local label="$1"
    local actual="$2"
    if [ "$actual" != "$expected" ]; then
        echo -e "${RED}FAIL${NC} $label: '$actual' != '$expected'"
        errors=$((errors + 1))
    else
        echo -e "${GREEN}OK${NC}   $label: $actual"
    fi
}

echo "Канон VERSION: $expected"
check_eq "python/pyproject.toml version"        "$(read_pyproject_version)"
check_eq "python/afb_bf_protocol/version.py"    "$(read_version_py)"
check_eq "spec/asyncapi.yaml info.version"      "$(read_asyncapi_version)"
check_eq "package.json version"                 "$(read_package_json_version)"

if [ "$errors" -ne 0 ]; then
    echo -e "${RED}Версии рассинхронизированы ($errors)${NC}" >&2
    exit 1
fi

echo -e "${GREEN}Все источники версии синхронны${NC}"
