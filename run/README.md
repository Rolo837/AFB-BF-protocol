# run/ — версионирование и релиз протокола

Канон semver-версии — корневой файл [`../VERSION`](../VERSION). Скрипты держат в
синхроне ещё 4 места: `python/pyproject.toml`, `python/afb_bf_protocol/version.py`,
`spec/asyncapi.yaml` (`info.version`), `package.json`. Правила уровней — [`../VERSIONING.md`](../VERSIONING.md).

## Модель веток

| Ветка | Роль |
|-------|------|
| `develop` | Разработка. Одна «покоящаяся» версия (последняя выпущенная), **не** тегируется покоммитно. AFB в git пинит `@develop`. |
| `main` | Выпущенные версии. Каждый релиз — тег `vX.Y.Z`, достижимый из `main` после merge. AFB `build.sh push` тянет протокол с `main`. |

## Скрипты

| Скрипт | Назначение |
|--------|-----------|
| `run/version.sh` | bump `patch`/`minor` / `set` / `show`; commit+push (`--no-commit` — только файлы) |
| `run/check-version.sh` | read-only проверка синхрона |
| `run/release.sh` | `tag` (тег на `develop`) / `publish` (merge `develop→main` + GitHub Release) |

AFB и BF **не** релизят протокол. Этот скрипт **не** правит пины потребителей
(`--afb` / `--bf` / `pin` убраны).

## Обычный релиз

```bash
# 1) канон изменён, codegen актуален, тесты зелёные
afb-bf-protocol-generate && pytest && npx @asyncapi/cli validate spec/asyncapi.yaml && npm run typecheck

# 2) версия (оформит CHANGELOG, commit+push; --no-commit — только файлы)
./run/version.sh minor              # или patch

# 3) тег на develop
./run/release.sh tag

# 4) после soak / когда main нужен облаку — стабильный релиз
./run/release.sh publish           # merge develop→main + GitHub Release (--generate-notes)
```

AFB на `develop` остаётся на `@develop` / `#develop`. Локальный тест:
`AFB/run/build.sh` (протокол с диска). Образы в репозиторий:
`AFB/run/build.sh push` (протокол с GitHub `main`).

Записи об изменениях — в `CHANGELOG.md` под `## Unreleased`, по ходу работы, без
версии; `version.sh` оформит под релиз. `--dry-run` есть у `tag` и `publish`.
