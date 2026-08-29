# run/ — версионирование и релиз протокола

Канон semver-версии — корневой файл [`../VERSION`](../VERSION). Скрипты держат в
синхроне ещё 4 места: `python/pyproject.toml`, `python/afb_bf_protocol/version.py`,
`spec/asyncapi.yaml` (`info.version`), `package.json`. Правила уровней — [`../VERSIONING.md`](../VERSIONING.md).

## Модель веток

| Ветка | Роль |
|-------|------|
| `develop` | Разработка. Одна «покоящаяся» версия (последняя выпущенная), **не** тегируется покоммитно. Потребители (AFB) в режиме разработки пинят `@develop`. |
| `main` | Выпущенные версии. Каждый релиз — тег `vX.Y.Z`, достижимый из `main` после merge. |

## Скрипты

| Скрипт | Назначение |
|--------|-----------|
| `run/version.sh` | bump `patch`/`minor` / `set` / `show`; правит `VERSION` + 4 синхронных места |
| `run/check-version.sh` | read-only проверка синхрона |
| `run/release.sh` | `tag` (тег `vX.Y.Z` на `develop`) / `publish` (merge `develop→main` + GitHub Release) |

## Обычный релиз

Как правило запускается **из единого комплекса AFB** — `AFB/run/release.sh tag --protocol {patch|minor}`,
который сам вызывает здешние `version.sh` / `release.sh`. Вручную:

```bash
# 1) канон изменён, codegen актуален, тесты зелёные
afb-bf-protocol-generate && pytest && npx @asyncapi/cli validate spec/asyncapi.yaml && npm run typecheck

# 2) версия (version.sh сам оформит ## Unreleased под vX.Y.Z)
./run/version.sh minor              # или patch
./run/check-version.sh
git commit -am "release vX.Y.Z"

# 3) тег на develop
./run/release.sh tag

# 4) после soak — стабильный релиз
./run/release.sh publish           # merge develop→main + GitHub Release (--generate-notes)
```

Записи об изменениях — в `CHANGELOG.md` под `## Unreleased`, по ходу работы, без
версии; `version.sh` оформит под релиз. `--dry-run` есть у `tag` и `publish`.
