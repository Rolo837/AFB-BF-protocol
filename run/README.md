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
| `run/release.sh` | `tag` (тег на `develop`) / `publish` (merge `develop→main` + GitHub Release) / `pin` (пины AFB/BF) |

AFB и BF **не** релизят протокол. Пины потребителей ставит **этот** скрипт
(`--afb` / `--bf`, по умолчанию выкл.).

## Обычный релиз

```bash
# 1) канон изменён, codegen актуален, тесты зелёные
afb-bf-protocol-generate && pytest && npx @asyncapi/cli validate spec/asyncapi.yaml && npm run typecheck

# 2) версия (version.sh сам оформит ## Unreleased под vX.Y.Z)
./run/version.sh minor              # или patch
./run/check-version.sh
git commit -am "release vX.Y.Z"

# 3) тег на develop; опционально сразу пин потребителей
./run/release.sh tag                # только тег
./run/release.sh tag --afb          # тег + пин AFB @vX.Y.Z + commit/push AFB@develop
./run/release.sh tag --afb --bf     # то же для AFB и BF

# если тег уже есть, а пин не ставили:
./run/release.sh pin --afb
./run/release.sh pin --bf

# 4) после soak — стабильный релиз (тег попадает в main — pip/npm #vX.Y.Z с main)
./run/release.sh publish           # merge develop→main + GitHub Release (--generate-notes)
```

`--afb` / `--bf` по умолчанию **выключены**. Соседний репозиторий должен быть
на `develop` с чистым деревом.

Записи об изменениях — в `CHANGELOG.md` под `## Unreleased`, по ходу работы, без
версии; `version.sh` оформит под релиз. `--dry-run` есть у `tag`, `publish` и `pin`.
