# Changelog

История версий протокола `afb-bf-protocol` (semver-теги пакета/спеки). Версия провода (`protocol` в конверте, поле `PROTOCOL_VERSION`) на всём этом диапазоне остаётся `afb.execution.v1` — ни один из релизов ниже не был проводным breaking change. Формат уровней версий — см. `VERSIONING.md`.

## v2.5.4 — 2026-08-15

PATCH (`afbws/instrument.channel.v1.json` — канал AFB-бэкенд↔AFB-фронтенд, не входит в `spec/asyncapi.yaml` и не пересекает провод AFB↔BF, `VERSIONING.md §2`): в модель каталога добавлен пропущенный уровень — **актив**, а канал `instrument` получил операции источников каталога. Актив — небольшой набор инструментов с общим источником ценообразования («Нефть Brent» = серии `BR-*` + `BRM-*`): он, а не тикер, лежит в подборке и он же несёт справочные данные (позиции, HHI). Серия входит в актив **целиком**, поэтому контракт, приехавший с суточным обновлением, принадлежит подборкам по определению, а не по эвристике совпадения. Актив всегда глобальный — личные подборки Фазы 3 собираются из тех же менеджерских активов. Пустая подборка, актив вне подборок и листинг вне активов — нормальные состояния, они остаются в снимке и видны менеджеру.

**Смена формы `setMembership` (`ticker` → `asset_id`) — коррекция неотгруженной операции, а не breaking change.** Операции `catalog`/`commit` выпущены в v2.5.3 несколькими часами ранее и не имеют ни одного клиента: фронтенд по-прежнему работает на legacy-`list`, единственный потребитель новой формы — бэкенд того же релиза. Поэтому required-поле правится на месте, без параллельной формы и без MAJOR. `x-afbws-support-id` (`afbws.instrument.channel.v1`) не менялся; версия провода (`afb.execution.v1`) не менялась, BF не затронут.

- **`spec/schemas/afbws/instrument.channel.v1.json`**:
  - `catalogAsset` — курируемый актив: `asset_id` (стабильный, генерирует сервер), `key` (читаемый слаг), `name`, `reference_series_code` (от какой серии брать справочные данные, если серий несколько; `null` — выбора нет), `archived`. Ни `scope`, ни владельца: активы всегда глобальные.
  - `assetMember` — ребро «актив → его член»: `asset_id`, `member_type` (`listing`|`series`), `member_ref` (канонический тикер либо `series_code`), `sort_order`. Порядок сквозной по обоим типам. Инвариант, который сервер проверяет: контракт не может входить в актив напрямую, если его серия уже член того же актива — «выдернуть» контракт из серии нечем.
  - `setMembership` — `ticker` → `asset_id`: подборка содержит активы, а инструменты следуют из актива. Это и есть то, что делает членство устойчивым к экспирациям.
  - `catalogResponse`/`commitResponse` — обязательные `assets[]` (`catalogAsset`) и `asset_members[]` (`assetMember`); `memberships` остаётся, но теперь это рёбра «подборка → актив». `items`/`series` не менялись. Обратите внимание: `assets` в новой форме — массив курируемых активов, а не legacy-словарь `series_code → {name}` из `list`.
  - `commitRequest` — секции `assets[]` (`assetUpsert`) и `remove_assets[]` (`asset_id`). `assetUpsert`: скаляры — патч, а `members` (`assetMemberInput`: `{member_type, member_ref}`) — **полный состав актива в нужном порядке**, как `membersEdit.order`, а не частичная правка. Удаление актива снимает его членство в подборках и его состав, но не трогает ни листинги, ни серии — они остаются как нераспределённые. Порядок применения секций зафиксирован в описании: `sets` → `remove_sets` → `assets` → `remove_assets` → `members` → `listings`/`archive_listings` → `series` (поэтому созданный в том же коммите актив можно тут же положить в созданную рядом подборку).
  - `membersEdit` — `add`/`remove`/`order` оперируют `asset_id`, а не тикерами.
  - `sources` (`afbws.instrument.sources.request/response.v1`, только менеджеру) — реестр источников каталога: `source_id`, `kind` (`moex`|`broker`), `title`, `available`, `last_refresh_at` (ISO-8601 UTC, `null` — ни разу), `listing_count` (сколько листингов сегодня числят этот источник владельцем торговых параметров). Недоступный источник тоже перечисляется: смысл операции — показать, **почему** ничего не обновляется.
  - `refresh` (`afbws.instrument.refresh.request/response.v1`, только менеджеру) — обновление каталога из выбранного источника по требованию, а не только суточным циклом. Запрос: `source_id` + `dry_run` (по умолчанию `false`). Ответ: `source_id`/`dry_run` эхом + `report` (`refreshReport`) — `applied`, `revision_before`/`revision_after` и списки `added`/`updated`/`resurrected`/`archived` (`{key, reason}`)/`new_series`/`absent_from_catalog`/`rows_without_series` плюс опциональные счётчики `changes`. Форма отчёта повторяет серверный `RefreshResult` по именам и смыслу; элементы списков — составные ключи каталога (`MIC:BOARD:TICKER`), потому что проводной `ticker` для MOEX схлопывается до голого символа и не различает доски. Предпросмотр (`dry_run: true`) строит тот же план и возвращает тот же отчёт, только не пишет: `applied: false`, `revision_after == revision_before`.
  - `errorResponse.details` (`errorDetails`) — новое опциональное поле `asset_ids` рядом с `set_ids`/`tickers`: у отклонённой правки теперь три уровня, и `validation_error` должен уметь назвать виновным именно актив. Enum кодов не менялся.
- **`ts/tools/generate-models.mjs`** — явные имена TS-типов для новых `$defs` (`InstrumentCatalogAsset`, `InstrumentAssetMember`, `InstrumentAssetMemberInput`, `InstrumentAssetUpsert`, `InstrumentCatalogSource`, `InstrumentSourcesRequest`/`Response`, `InstrumentRefreshRequest`/`Response`, `InstrumentRefreshReport`, `InstrumentRefreshArchivedEntry`) вместо автоимён вида `AfbwsInstrumentChannelV1_CatalogAsset`.
- **Сгенерировано** (`afb-bf-protocol-generate`): `ts/src/models.ts`, `python/afb_bf_protocol/models_generated.py`, зеркало `python/afb_bf_protocol/schemas/`.
- **`python/tests/test_afbws_instrument_channel_schema.py`** — позитив/негатив на каждый новый `$def` и на обе новые пары схем; отдельно зафиксировано, что `setMembership` больше не знает поля `ticker`, что `member_type` вне enum отклоняется и что `refresh` без `source_id` невалиден.
- **Версии**: bump до `2.5.4` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.5.3 — 2026-08-14

PATCH (`afbws/instrument.channel.v1.json` — канал AFB-бэкенд↔AFB-фронтенд, не входит в `spec/asyncapi.yaml` и не пересекает провод AFB↔BF): канал `instrument` получил операции федеративного каталога Фазы 2 — `catalog`/`commit`/`user`. Новая форма описывает каталог как произвольные пересекающиеся **подборки** (`catalogSetEntry` + `setMembership`) вместо дерева `group` с единственным родителем, плюс независимую ось серий фьючерсов (`catalogSeries`, вместо `asset`). Деления на «системные» и «глобальные» подборки нет: `scope` — только `global` (курирует менеджер) или `user` (личные подборки Фазы 3). Правка полностью аддитивна: ни один существующий `$def` не удалён и не переименован, ни одно опциональное поле не стало обязательным, `x-afbws-support-id` (`afbws.instrument.channel.v1`) не менялся.

- **`spec/schemas/afbws/instrument.channel.v1.json`**:
  - `catalog` (`afbws.instrument.catalog.request/response.v1`) — полный снимок каталога в новой форме для любого авторизованного вызывающего: `items` + `sets` + `memberships` + `series`, со штампом `catalog_revision`. Авторитетное членство несёт только `memberships`; поле `group` внутри `items[]` — legacy-остаток для клиентов, оставшихся на `list`, и в этой форме не читается. Листинг без единого членства нормален и виден менеджеру.
  - `commit` (`afbws.instrument.commit.request/response.v1`) — единственная запись глобального каталога, только для менеджера: дельта (`sets`/`remove_sets`/`members`/`listings`/`archive_listings`/`series`/`reason`) поверх обязательного `base_revision` (CAS). Расхождение ревизии — `conflict`, актуальная ревизия приезжает в `errorResponse.details.catalog_revision`. Ответ — полный новый снимок (та же форма, что у `catalog`) плюс опциональные счётчики `applied` (как в `catalog_audit.summary`). В `listings` переиспользуется `instrument.v1.json` ради его class-gating (`futures`-only поля, `isin` только для `stock`); поле `group` элемента при этом игнорируется — членство задаётся только через `members`.
  - `user` (`afbws.instrument.user.request/response.v1`) — личные подборки и overlay (`userState`: `revision`/`sets`/`memberships`/`hidden_set_ids`/`order`) с собственным `base_revision` личного агрегата, независимым от `catalog_revision`. Объявлено сейчас, чтобы клиенты писались против финальной формы; бэкенд Фазы 2 отвечает `unsupported_action`.
  - `errorResponse` — новое опциональное поле `details` (`errorDetails`: `catalog_revision`/`user_revision`/`set_ids`/`tickers`). Enum кодов не менялся.
  - `list`/`apply` **не удалены**, только помечены `DEPRECATED` в `description`: `list` бэкенд продолжает обслуживать для фронтендов старше `catalog`, `apply` перестаёт (`unsupported_action`), схема оставлена, чтобы запрос старого фронтенда разбирался в типизированную ошибку, а не в `invalid_schema`. `get`/`pool`/`resolve`/`detail` не менялись.
- **`ts/tools/generate-models.mjs`** — явные имена TS-типов для всех новых `$defs` (`InstrumentCatalogSetEntry`, `InstrumentSetMembership`, `InstrumentCatalogSeries`, `InstrumentCatalogSeriesMap`, `InstrumentUserState`, `InstrumentErrorDetails`, `InstrumentCatalogRequest`/`Response`, `InstrumentCommitRequest`/`Response`, `InstrumentSetUpsert`, `InstrumentMembersEdit`, `InstrumentListingArchival`, `InstrumentSeriesUpsert`, `InstrumentUserRequest`/`Response`) вместо автоимён вида `AfbwsInstrumentChannelV1_CommitRequest`.
- **Сгенерировано** (`afb-bf-protocol-generate`): `ts/src/models.ts`, `python/afb_bf_protocol/models_generated.py`, зеркало `python/afb_bf_protocol/schemas/`.
- **`python/tests/test_afbws_instrument_channel_schema.py`** — позитив/негатив на каждый новый `$def`.
- **Версии**: bump до `2.5.3` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.4.6 — 2026-08-07

PATCH (не пересекает канал AFB↔BF — правка ручного core-кода `python/afb_bf_protocol/`, не схем): `amend_rules.py::_entry_triggers` каноникализирует ногу входа перед сравнением, когда `left.source == "immediate"` — приводит к `{"left": {"source": "immediate"}}`, отбрасывая `right`/`op`/`id`/`duration`. Раньше сравнение было сырым структурным `!=` по всему `condition`-словарю, включая `right`/`op` immediate-ноги — а они по конвенции протокола (`condition.v1.json`'s `immediateExpr`, `condition_semantics.py`) структурные плейсхолдеры без смысла, которые никогда не должны читаться. Как только формат этого плейсхолдера у AFB-компилятора стал зависеть от того, как рыночный вход попал на вход компиляции (легаси zero-const сентинел vs прямой `immediate` в плане, protocol v2.4.5), одна и та же по смыслу нога входа при перекомпиляции стала давать разные строки (`right.const`: `"0"` vs `"0.0"`/`"0.00"`), и `evaluate_amend` ложно фиксировал «entry изменился» — блокируя amend/перемещение примитива для СЛ/ТП, holding-сделок с рыночным входом, даже когда entry никто не трогал.

- **`python/afb_bf_protocol/amend_rules.py`** — новая функция `_canonical_entry_condition`, применена в обеих ветках `_entry_triggers` (v2-список и v1-объект).
- **Версии**: bump до `2.4.6` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.4.5 — 2026-08-07

PATCH: `tradeplan.v2.json` (AFB-only, не пересекает канал AFB↔BF) — `tpConditionNode.left` теперь допускает `condition.v1.json#/$defs/immediateExpr` (`{"source": "immediate"}`) на ноге входа, в дополнение к price/indicator/dataset-выражениям. Раньше рыночный вход в плане мог кодироваться только устаревшим сентинелом (price-условие с нулевой константой), а `immediate` появлялся лишь в скомпилированной сделке — эта запись отражает реальную семантику AFB напрямую в плане, а не только в её производной. `right`/`op` на такой ноге — структурные плейсхолдеры без смысла (как и в `deal.v2.json`), значимо только на входе — AFB/BF отклоняют это на стоп-лоссе/тейк-профите. Полная матрица допустимости по-прежнему проверяется после компиляции `deal.v2.json`+BF, не здесь.

- **`spec/schemas/tradeplan.v2.json`** — `immediateExpr` добавлен в `oneOf` поля `left`; уточнено описание схемы и `tpConditionNode.left`.
- **Версии**: bump до `2.4.5` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.4.4 — 2026-08-07

PATCH: `tradeplan.v2.json` (AFB-only, не пересекает канал AFB↔BF) получил опциональное поле `editor` (`simple`/`advanced`) — какой из двух режимов редактора AFB-фронтенда владеет планом. Никогда не копируется в скомпилированную сделку. Отсутствие поля означает `advanced` (планы, сохранённые фронтендом старше этого поля, открываются расширенным редактором). Часть отказа от формата торговых планов v1 — оба режима редактора AFB работают теперь только с `afb.tradeplan.v2`, а `editor` заменяет прежний дискриминатор «версия схемы» как признак режима UI.

- **`spec/schemas/tradeplan.v2.json`** — новое опциональное поле `editor`.
- **Версии**: bump до `2.4.4` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.4.3 — 2026-08-06

PATCH: `gp.v1.json` (AFB-only) — уточнён `description` поля `tradeplan_id`: архивация плана больше НЕ переписывает его условия в числовые значения. Уровни плана по-прежнему физически удаляются из живого хранилища примитивов при архивации, но сам план сохраняет исходные ссылки на примитив (`condition_type: 'primitive'` / `right.primitive_id`) — историческую отрисовку несёт полная копия каждого уровня в `archived_components` плана (AFB-side, вне протокола), а не переписанные числа в условии. Чисто описательное уточнение — форма самой схемы не менялась.

## v2.4.2 — 2026-08-06

PATCH: `gp.channel.v1.json` (AFB-only, не пересекает канал AFB↔BF) получил первый push-тип — `afbws.gp.sync.push.v1`. Server-initiated, без `request_id`, `items[]` — авторитетный апсерт `afb.gp.v1` по `id`, никогда снимок. Закрывает разрыв, из-за которого владение примитивом (`tradeplan_id`, добавлено в `v2.4.1`), меняющееся при публикации/amend сделки или физическом удалении плана, не доходило до фронтенда без перезагрузки — эти операции идут через каналы `deal`/`tradeplan`, а не `gp`. Удаление примитива при заморозке архивируемого плана этим пушем сознательно не передаётся: такой примитив всегда был привязан к плану и виден только при выбранном плане, а сам план в этот момент уже получает свой `afbws.tradeplan.sync.push.v1` со статусом `archived`.

- **`spec/schemas/afbws/gp.channel.v1.json`** — новый `$defs/syncPush`, добавлен в `oneOf` канала.
- **Версии**: bump до `2.4.2` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.4.1 — 2026-08-05

PATCH: `gp.v1.json` (AFB-only, не пересекает канал AFB↔BF) получил опциональное поле `tradeplan_id` — владеющий торговый план примитива. Проставляется сервером при компиляции плана в сделку (публикация/amend), снимается только при физическом удалении плана; клиент это поле не задаёт. Пустое/отсутствующее значение — свободный примитив, доступный любому плану. Отдельно от уже существующего вычисляемого «упомянут ли примитив в условии плана» (по-прежнему не персистится) — это новое поле про физическое владение.

- **`spec/schemas/gp.v1.json`** — новое опциональное поле `tradeplan_id`; уточнён `description` (владение персистится, ссылка из условия — по-прежнему вычисляется на лету).
- afbws-схема канала `gp` (`spec/schemas/afbws/gp.channel.v1.json`) не менялась — все её `get`/`list`/`set`-формы уже ссылаются на `gp.v1.json` через `$ref`, поле подхватывается автоматически.
- **Версии**: bump до `2.4.1` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.4.0 — 2026-08-05

MINOR: новое опциональное поле `quantity` в `deal.snapshot`/`deal.status_changed` — финальный (resolved) размер сделки, который BF фиксирует один раз в момент триггера входа (`resolved_quantity`), в отличие от предварительной publish-оценки `broker_sizing.lots`.

- **`spec/schemas/payloads/deal.snapshot.json`** (новый файл) — payload `deal.snapshot` вынесен из инлайновой схемы `asyncapi.yaml` в отдельный файл (был пустым стабом без примера, `additionalProperties: true`, в отличие от соседних сообщений) — те же поля (`deal_id`, `status`, `execution_phase`, `observed`, `positions[]`) плюс новый опциональный `quantity` (integer).
- **`spec/schemas/payloads/deal.status_changed.json`** — новый опциональный `quantity` (integer) — тот же смысл, реальный проактивный канал доставки (сообщение шлётся на каждом переходе состояния сделки, в т.ч. сразу после фиксации `resolved_quantity`), в отличие от `deal.snapshot`, который сегодня шлётся только по явному on-demand `deal.operation{op:"reconcile"}`.
- **`spec/schemas/afbws/deal.channel.v1.json`** — `$defs.dealSizingDisplay` (AFB frontend↔backend, не пересекает канал AFB↔BF) получил опциональный `resolved_lots` (integer) рядом с `lots`/`required_cash` — публичная проекция того же `quantity`, отдаваемая `deal_summary`/`deal_detail`.
- **`examples/_payloads/deal.snapshot.json`** (новый) — первый пример для `deal.snapshot`.
- **Перегенерировано**: `taxonomy.py`/`MESSAGES.md`/`ts/src/taxonomy.ts`/`index.ts`/`models_generated.py`/`ts/src/models.ts`/schemas mirror, `examples/deal.snapshot.json`.
- **Версии**: bump до `2.4.0` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.3.1 — 2026-08-03

PATCH: согласование интервала heartbeat при handshake и deprecation split-полей `dry_run_*`/`margin_trading_*`.

- **`spec/schemas/payloads/session.hello.json`** — опциональный `heartbeat_interval_sec` (предложение BF; AFB может clamp в `hello_ack`).
- **`spec/schemas/payloads/session.hello_ack.json`** — уточнён description `heartbeat_interval_sec` (нормализованный интервал); `dry_run_afb`/`dry_run_bf`/`margin_trading_afb`/`margin_trading_bf` помечены `deprecated` (использовать эффективные `dry_run`/`margin_trading`).
- **`spec/schemas/afbws/bfs.registry.v1.json`** — `dry_run_afb`/`dry_run_bf` deprecated.
- **`spec/schemas/afbws/link.status.v1.json`** — description `heartbeat_interval_sec`: negotiated interval для stale (3×) и UI.
- **`docs/PROTOCOL.md`** — handshake: предложение/нормализация heartbeat; split-поля deprecated.
- **Версии**: bump до `2.3.1` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.3.0 — 2026-08-02

MINOR: часть 1 (протокол) миграции канала `account` для AFB frontend↔backend — новый schema-first `afbws.account.channel.v1`, мультисчётность на проводе AFB↔BF (read-only: коннектор видит все счета брокерского токена, но исполняет по-прежнему только на своём торговом) и закрытие семейства `broker.*` payload-схемами: у каждого типа теперь есть `spec/schemas/payloads/<type>.json`, ранее было только у пяти из двенадцати.

- **`spec/schemas/payloads/broker.get_accounts.json`, `broker.accounts.json`** (новые) — `broker.get_accounts`/`broker.accounts` (afb2bf/bf2afb): `broker.accounts` несёт `default_account_id` (единственный торговый счёт BF), `as_of` и полный `accounts[]` (`account_id`, `tradable`, `readonly`, `status`, `equity`, `cash[]`, `positions[]`). В отличие от `broker.account`, здесь **нет** `broker_account_id` — дублирование двух идентификаторов одного счёта в старом типе признано путаницей и сознательно не перенесено. `additionalProperties: false` — инвариант проверяется тестом (`test_broker_account_payload_schema.py::test_accounts_rejects_broker_account_id`).
- **`spec/schemas/payloads/broker.get_account.json`, `broker.account.json`, `broker.get_orders.json`, `broker.orders.json`, `broker.get_catalog.json`, `broker.get_instrument.json`, `broker.resolve_instrument.json`** (новые) — недостающие payload-схемы для уже существующих типов, описывающие фактическую форму `belphegor/reporting/broker_snapshots.py` (`account_snapshot_payload`/`stored_orders_payload`) без изменения поведения на проводе.
- **Deprecated** (тег в спеке + описание замены, тип остаётся в таксономии — удаление запрещено без отдельного MAJOR): `broker.get_account`/`broker.account` (заменены `broker.get_accounts`/`broker.accounts`), `broker.get_instrument`/`broker.instrument` (заменены уже существующей парой `broker.resolve_instrument`/`broker.instrument_resolved`, которую `afbws.instrument.channel.v1` использует для detail-запросов и раньше).
- **`spec/schemas/payloads/daemon.capabilities.json`** — `features.multi_account` (BF реализует `broker.get_accounts`/`broker.accounts`) и документированный `account_id` (был не объявлен, хотя всегда присылался).
- **`spec/schemas/payloads/session.hello_ack.json`** — `features.multi_account` (AFB согласилось принимать `broker.accounts`). Обязательный двусторонний хендшейк: BF шлёт `broker.accounts` только сессии, объявившей `features.multi_account` в `hello_ack`, и не шлёт ей одновременно устаревший `broker.account` — иначе `broker.accounts`, отправленный старому AFB, обрывает BF-линк (`verify_incoming` в `AFB/backend/trade/service.py` бросает на неизвестном типе, `bf_ws.py` закрывает соединение).
- **`spec/schemas/deal.v1.json`** — опциональный `target.account_id` (переиспользуется `deal.v2.json` через существующий `$ref`); BF уже читает это поле (`plan_validation.py`: `binding.account_id or target.account_id`), но оно не было задекларировано.
- **`spec/schemas/tradeplan.v1.json`, `tradeplan.v2.json`** — опциональный `account_id` рядом с `connector`; пусто/отсутствует = дефолтный (торговый) счёт коннектора, резолвится на лету при публикации, офлайн-миграция сохранённых планов не проводится.
- **`spec/schemas/afbws/account.channel.v1.json`** (новый, capability `afbws.account.channel.v1`) — `list`/`get`/`orders`/`events` + typed `error`, push `snapshot`/`orders`. Полностью типизированные AFB-проекции (`accountSnapshot`, `order`, `eventRecord`), не проброс BF-формы — по аналогии с `deal.public.v1.json`. Заменяет для negotiated-клиентов legacy `channel=account, type=get_account|get_orders|get_events`; `get_catalog`/`get_instrument`/`resolve_instrument` в миграцию не входят — уже перекрыты `afbws.instrument.channel.v1`.
- **Удалены черновики** `spec/schemas/afbws/account.snapshot.v1.json`, `account.orders.v1.json`, `account.catalog.v1.json`, `account.instrument.v1.json`, `account.events.v1.json` — не были описаны в `ENTITY_WS_PROTOCOL.md`/использовались как непрозрачный proxy BF-формы (`data: additionalProperties: true`). `$defs/record` из `account.events.v1.json` перенесён в `account.channel.v1.json` под тем же экспортным именем `AccountEventRecord`.
- **Перегенерировано**: `taxonomy.py`/`taxonomy.ts`/`MESSAGES.md`/`capabilities.py`/`capabilities.ts`/`index.ts`/`models_generated.py`/`ts/src/models.ts`/schemas mirror. Новая константа `ACCOUNT_CHANNEL_V1`.
- **Версии**: bump до `2.3.0` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

Бэкенд/фронтенд AFB и read-only мультисчётность в BF — отдельными фазами того же плана, вне этого тега; capability `afbws.account.channel.v1` пока нигде не рекламируется.

## v2.2.0 — 2026-07-31

MINOR: новое опциональное поле `logic` на каждом элементе многоуровневых списков `entry`/`stop_loss`/`take_profit` в `afb.deal.v2` и `afb.tradeplan.v2` — инфиксный оператор (`split`/`and`/`or`) связи ноги с предыдущей в том же списке. Обратно совместимое расширение протокола AFB↔BF: поле опционально, отсутствие ≡ `split` ≡ сегодняшнее поведение (доли объёма по `percent`), старые сделки и планы не мигрируют.

- **`spec/schemas/deal.v2.json`** — новый `$defs.legJoin` (`enum: [split, and, or]`) и опциональное `logic` на элементах `entry`/`stop_loss`/`take_profit`. Грамматика (описана в `legJoin.description` и `docs/PROTOCOL.md` §17): подряд идущие ноги, связанные `and`, образуют **группу** — гейтующие подусловия одной заявки на весь объём группы, срабатывает только когда все истинны одновременно; подряд идущие группы, связанные `or`, образуют **корзину** — независимые заявки, делящие общий бюджет объёма (первый филл гасит остальные); `split` начинает новую корзину, корзины делят объём роли по `percent` (текущее поведение). `percent` осмыслен только на первой ноге корзины, на присоединённых `and`/`or` — не допускается. Первая нога списка `logic` не несёт. Позиционные правила (первая нога, однородность значения в пределах роли — временное ограничение BF) схемой не проверяются, как и остальные зависящие от места правила этого вокабуляра — это ответственность потребителя. Логика не влияет на тип заявки (LIMIT/MARKET) — тот по-прежнему решает только оператор условия.
- **`spec/schemas/tradeplan.v2.json`** — то же поле, `$ref` на `deal.v2.json#/$defs/legJoin`; AFB переносит его через компиляцию без изменений на соответствующую ногу `deal.v2`.
- **`docs/PROTOCOL.md`** — §17 переписан под инфиксную семантику: разбор списка ног в группы/корзины, приоритет `and` > `or` > `split`, пример `a ИЛИ (b И c)`, явная фиксация того, что поле не меняет вокабуляр условий (`condition.v1.json` не тронут) и не вводит групповые узлы условия на проводе — группировка для `and` остаётся деталью исполнения BF.
- **`python/afb_bf_protocol/amend_rules.py`** — `_entry_triggers` включает `logic` в проекцию каждой ноги (наравне с `percent`/`condition`), чтобы смена связи между ногами считалась изменением поля `entry` и подпадала под тот же фазовый гейт amend, что и смена условий; `_stops`/`_takes` уже сравнивают ноги целиком (включая `logic`), правки не потребовалось.
- **`examples/_payloads/deal.publish__v2_any_entry.json`** (новый) — сделка с двумя touch-уровнями входа, вторая нога `logic: "or"`, без `percent`. **`examples/tradeplans/tradeplan.v2.leg-logic.json`** (новый) — план с `entry` из двух ног (`or`) и `stop_loss` из ценового уровня и индикаторного пересечения (`and`).
- **Перегенерировано**: `python/afb_bf_protocol/models_generated.py` (`DealV2LegJoin`, поле `logic` на элементах списков `DealV2`/`TradePlanV2`), `ts/src/models.ts` (`DealV2_LegJoin`). `taxonomy.py`/`docs/MESSAGES.md`/`capabilities.py` не изменились — набор типов сообщений не тронут.
- **Версии**: bump до `2.2.0` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.1.3 — 2026-07-30

PATCH (по явному решению релиза): часть 1 (протокол) плана `deal-channel-migration_97a53aa5` — schema-first канал `deal` для AFB frontend↔backend (AFB-only, никогда не пересекает канал AFB↔BF) и типизация `source` в `afb.deal.v1/v2`. `source` и раньше принимался на проводе как открытый нетипизированный объект (схема не ограничивала его `additionalProperties`) — `tradeplan_id` формализует уже фактически передаваемое поле, а не добавляет новое обязательство для BF; расширение остаётся необязательным и не меняет поведение существующих BF.

- **`spec/schemas/deal.v1.json`, `spec/schemas/deal.v2.json`** — новый опциональный `source` (`tradeplan_id` — единственный источник истины связи сделка→план; legacy `kind`/`draft_id` описаны как deprecated, для старых непромигрированных записей). Не в корневом `required` — старые AFB продолжают публиковать сделки без `source` или с legacy-полями.
- **`spec/schemas/afbws/deal.public.v1.json`** (новый) — строгая public-проекция `ExecutionDeal` (v1/v2): обязательный `source.tradeplan_id`, без `owner`/`archive_reason`/compile-метаданных/`source.kind`/`draft_id`.
- **`spec/schemas/afbws/deal.channel.v1.json`** (новый, capability `afbws.deal.channel.v1`) — `get`/`list` (публичные `dealSummary`/`dealDetail`, без `source_refs`/`status_history`/`event_journal`/`orders`/`positions`/`observed`), `publish`/`rebind` (только ссылка на сохранённый план, без inline draft), `operation` (enum `action`, `archive` зарезервирован как `unsupported_action`), `amend` (уже в форме фазы B: `deal_edit`/`drop_overrides`/`base_revision`), typed `error`, гарантированные `triggered`/`ack` (аналог alarm). `dealSummary`/`dealDetail` несут публичный `realized_pnl` (проекция внутреннего `source_refs.afb_pnl`) и `dealDetail.overrides` — карту override-значений **в форме плана** (не только имена полей — см. `plans/gentle-spinning-wigderson.md` §B.0, чтобы редактору не понадобился decompiler deal→plan).
- **`spec/schemas/afbws/deal.record/pnl/event.v1.json`** — переведены на `channel`+`schema`; `deal.record` теперь несёт публичную проекцию `dealDetail`, а не `deal_state.v2.json`.
- **`spec/schemas/afbws/common.v1.json`** — добавлены коды ошибок `forbidden`, `bf_offline`, `unsupported_action`.
- **`python/afb_bf_protocol/amend_rules.py`** — новая `editable_fields_for(ctx, fields=...)`: какие поля матрицы редактируемы в текущей фазе/статусе без пробного сравнения — нужна public-проектору AFB для `dealDetail.editable_fields`.
- Исправлен баг `ts/tools/generate-models.mjs`: `$defs`-алиас на корень другого файла целиком (без фрагмента) собирал битый ключ типа — обойдено прямым `$ref`.
- **Перегенерировано**: `taxonomy.py` / `MESSAGES.md` / `ts/src/*` / `models_generated.py` / schemas mirror.
- **Версии**: bump до `2.1.3` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

Бэкенд/фронтенд AFB для этой миграции — отдельно, вне тегов протокола; capability `afbws.deal.channel.v1` пока нигде не рекламируется (backend `BACKEND_SUPPORTED_CAPABILITIES` её не содержит) — включение отложено до завершения фронтенд-части и офлайн-миграции `state/deals/**/*.yaml`.

## v2.1.2 — 2026-07-27

PATCH (по явному решению релиза; формально новый тип сообщения — MINOR): канонический NACK на `broker.*` команды — `broker.error`. Обратно совместимо: старые BF могут по-прежнему слать `deal.rejected` на broker-команды; потребители принимают оба типа на переходный период.

- **`spec/schemas/payloads/broker.error.json`** (новый) — required `code`, `command_type`; optional `message`, `at`. Без `deal_id`.
- **`spec/asyncapi.yaml`** — сообщение `broker.error` (user/bf2afb), канал + `receiveFromBf`.
- **`docs/PROTOCOL.md` §4.5** — ошибка любой `broker.*` → `broker.error`.
- **`examples/broker.error.json`** — подписанный пример (`broker_disconnected` / `broker.get_account`).
- **Перегенерировано**: `taxonomy.py` / `MESSAGES.md` / `ts/src/*` / `models_generated.py` / schemas mirror.
- **Версии**: bump до `2.1.2` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.1.1 — 2026-07-26

PATCH: часть фазы A1 сепарации торгового плана и сделки (AFB) — новая статусная модель `afb.tradeplan.v1/v2` и переопределение семантики `tradeplan/sync`-пуша. Эти схемы AFB-стороннего фронтенд↔бэкенд взаимодействия (`tradeplan.*` никогда не пересекают канал AFB↔BF), поэтому изменение не затрагивает провод и BF не обновляет пин.

- **`spec/schemas/tradeplan.v1.json`, `spec/schemas/tradeplan.v2.json`** — `status.enum`: `["new","active","published","closed","expired"]` → `["draft","published","completed","archived"]` (несовместимое сужение набора значений поля, которое никогда не пересекает AFB↔BF — по правилам версионирования расширения, специфичные для связки фронтенд↔бэкенд AFB, это PATCH). Добавлены `archived_at` (метка ручной архивации) и `instrument_missing` (не персистится; накладывается AFB при выдаче списка планов, если тикер отсутствует в справочнике securities — раньше для этого перегружался статус `expired`, которого больше нет).
- **`spec/schemas/afbws/tradeplan.channel.v1.json`** — добавлена пара `afbws.tradeplan.archive.request.v1`/`afbws.tradeplan.archive.response.v1` (ручная архивация плана, гейтуется живыми сделками). Переопределена семантика `syncPush` (`afbws.tradeplan.sync.push.v1`): `items[]` теперь ДЕЛЬТА (upsert по `id`), а не снимок всего списка — синтаксис сообщения не изменился, обновлены только `title`/`description`. Полный список планов выдаёт только `afbws.tradeplan.list.request.v1`; удаление плана этим пушем не передаётся.
- **Перегенерировано**: `python/afb_bf_protocol/schemas/` (мирроринг), `ts/src/models.ts`.
- **Версии**: bump до `2.1.1` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.1.0 — 2026-07-25

MINOR: новый AFB-пушный фид датасетов MOEX/Algopack (`dataset.update`), резервный `dataset.subscribe`, `deal.signal` помечен deprecated. Обратно совместимое расширение протокола AFB↔BF — новые опциональные типы сообщений, ни один существующий формат не тронут.

Мотивация: у BF нет и не будет доступа к бирже/Algopack (токен привязан к IP AFB), поэтому dataset-ветка `condition.v1.json` не могла вычисляться на стороне BF. Прежняя схема — `deal.signal`, где AFB сам оценивал dataset-условие и слал разовый сигнал по факту срабатывания, — заменяется фидом снапшотов: AFB толкает демону актуальные срезы нужных датасетов, а BF вычисляет условие сам через общую `condition_semantics`, как и все прочие источники (price/indicator).

- **`spec/schemas/payloads/dataset.update.json`** (новый, `system`/`afb2bf`) — `datasets[]`: `dataset_id` (`positions`/`orders`/`hhi`/`trades` — без `volume`, он объявлен в `condition.v1.json`, но не вычисляется ни AFB, ни BF), `instrument` (`$ref` на `deal.v1.json#/$defs/instrument`, не дублируется), `as_of` (ISO-время среза на бирже), `stale_after_sec` (TTL, задаёт AFB), `current`/`previous` (словари «поле датасета → число»; `previous` опционален, нужен только cross-операторам). Snapshot-семантика: каждый `dataset.update` несёт **полный** набор записей для данного BF, получатель **замещает** кэш целиком (replace-all, не merge); пустой массив — валиден, означает «ничего не нужно».
- **`spec/schemas/payloads/dataset.subscribe.json`** (новый, `system`/`bf2afb`) — **RESERVED, не реализовано**: зарезервированная возможность BF запросить у AFB дополнительную подписку на датасет; сейчас AFB сам выводит потребность из условий опубликованных сделок, BF ничего не отправляет, AFB не обязан обрабатывать. Фикстура не создавалась.
- **`spec/asyncapi.yaml`** — добавлены каналы/операции/`components.messages` для `dataset_update` (`sendToBf`) и `dataset_subscribe` (`receiveFromBf`); `deal_signal` помечен тегом `deprecated`, описание обновлено: «DEPRECATED: superseded by the dataset.update feed (BF evaluates dataset conditions itself); kept for wire compatibility, no longer sent by AFB» (тип не удалён — удаление типа является MAJOR и запрещено по умолчанию).
- **`docs/PROTOCOL.md`** — новый §16 «Dataset feed (`dataset.update` / `dataset.subscribe`)»: назначение, кто определяет потребность (AFB — из условий опубликованных сделок, все ноги entry/stop_loss/take_profit, обе стороны сравнения), snapshot-семантика, staleness (`now <= as_of + stale_after_sec`, иначе данные считаются отсутствующими и условие даёт `false`; сделка при этом не ставится на паузу, оценка возобновляется автоматически при свежих данных), `current`/`previous` и cross-операторы, ключевание по `instrument` (AFB сам резолвит биржевую номенклатуру, например futures-позиции ключуются базовым активом, а не кодом контракта), текущая/планируемая частота обновления биржи (без хардкода на BF — TTL приходит в сообщении), `dataset.subscribe`. §4.4 и таблица в §12 приведены в соответствие (deprecated `deal.signal`; dataset-условия вычисляет BF по данным фида, `volume` по-прежнему не поддержан).
- **`examples/_payloads/dataset.update.json`** — новый пример (позиции по фьючерсу с `previous`, `hhi` без `previous`); `python -m afb_bf_protocol.tools.make_fixtures` пересобрал подписанный `examples/dataset.update.json`.
- **Перегенерировано**: `python/afb_bf_protocol/taxonomy.py`, `docs/MESSAGES.md`, `python/afb_bf_protocol/schemas/` (мирроринг), `ts/src/taxonomy.ts`/`ts/src/index.ts`, `ts/src/models.ts`, `python/afb_bf_protocol/models_generated.py`.
- **Версии**: bump до `2.1.0` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`. Версия провода (`afb.execution.v1`) не менялась.

## v2.0.10 — 2026-07-23

PATCH: `deal.report` — `fills[]` переведены на trade-based формат (один элемент на брокерский трейд, а не на ордер), удалены `fills[].commission` и блок `summary` целиком. Wire AFB↔BF не тронут семантически — только сужение формата уже нетребуемых полей.

Мотивация: у Финама `SubscribeTrades` даёт по несколько трейдов на один ордер (BF раньше агрегировал только первый); `summary` (`entry/exit_avg_price`, `realized_pnl`, `total_commission`) почти всегда приходил `null`-ами — расчёт реализованной прибыли переносится на AFB (леджер по фактам исполнения, средневзвешенная цена входа), справочное сверочное значение теперь берётся из `position.closed.realized_pnl`. Комиссии — вне скоупа.

- **`spec/schemas/payloads/deal.report.json`** — в `fills[]` item добавлено опциональное `trade_id` (**не** в `required`: старые BF, ещё не персистящие трейды, продолжают присылать payload без него — толерантность к разнородному парку); удалено `fills[].commission`; удалён блок `summary` из `properties` целиком; обновлены описания (`fills` — trade-based, у Финама N трейдов на ордер → N элементов; top-level `description` фиксирует, что `summary` удалён как не имевший потребителей).
- **Обоснование PATCH, а не MAJOR**: `summary` никогда не входил в `required`, схема несёт `additionalProperties: true` — старый payload (с `summary`/`commission`) валиден против новой схемы, новый payload (с `trade_id`, без них) валиден против старой. Двусторонняя валидность подтверждена явной формальной проверкой (`test_fixtures_schema.py`, `test_equivalence.py`), реальных потребителей `summary`/`commission` не найдено (правятся в AFB тем же релизным шагом: ридер `service.py` и фронтовый `dealReportCommission`).
- **`examples/_payloads/deal.report.json`** — фикстура приведена к новому формату: `fills[]` несёт `trade_id` (синтетический `synth-{order_id}`, у примера цена ещё `null` — до-B1-фолбэк арена-сделка), `commission`/`summary` убраны.
- **Перегенерировано**: `python/afb_bf_protocol/schemas/` (мирроринг), `python/afb_bf_protocol/models_generated.py` (`Fill.trade_id`, тип `Summary` исчез), `ts/src/models.ts` (аналогично), `examples/deal.report.json` (пересобранный подписанный конверт). `taxonomy.py`/`docs/MESSAGES.md`/`capabilities.py` не изменились — набор типов сообщений не тронут.
- **Версии**: bump до `2.0.10` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`.

## v2.0.9 — 2026-07-23

PATCH: новый `conditionNode` источник `immediate` — явный вход/условие «по рыночной цене», без ценового уровня. Обратно совместимое расширение вокабуляра (условие AFB↔BF). Прежний sentinel (`price`/`touch`-или-`above` против нулевой константы, `TradeService._normalize_market_entry_event`) по-прежнему принимается на чтение бессрочно — уже сохранённые сделки/тредплены в этом виде не мигрируют.

Мотивация: `right.const == 0` — не цена, а маркер отсутствия уровня; читать его как цену молча ломало риск-сайзинг (`deal-d90e-4c2d-be3d`: BF трактовал 0 как ценовой уровень, `resolve_lots` падал с `SizingError`, вход не размещался часами без единого сигнала). Новый источник убирает необходимость угадывать интент по нулю — `left.source == "immediate"` читается напрямую, `op`/`right` остаются пустыми заглушками ради структурной совместимости `oneOf`, их значение не имеет смысла и не должно читаться.

- **`spec/schemas/condition.v1.json`** — новый `$defs.immediateExpr` (`{source: "immediate"}`) и шестая ветка `oneOf` в `conditionNode`: `left` — `immediateExpr`, `op` зафиксирован как `"above"` (заглушка), `right` — `rightConst` (заглушка), `timeframe` запрещён. Существующие пять веток не тронуты — `oneOf` остаётся однозначным по `left.source`. Роль (только `entry`, не `stop_loss`/`take_profit`) и запрет `duration` — на уровне потребителей (`protocol/validation.py` на стороне BF), не схемы, как и для прочих условий, зависящих от того, где узел расположен.
- **`spec/schemas/deal.v1.json`** — собственный (замороженный) `conditionNode.left.source` расширен с `const: "price"` до `enum: ["price", "immediate"]`. `op`/`required` не менялись.
- **`python/afb_bf_protocol/condition_semantics.py`** — новая `IMMEDIATE_OPS = {"above"}`, `OPS_BY_SOURCE["immediate"]`, функция `evaluate_immediate(cur) -> bool` (`cur is not None and cur > 0`) — единая точка истины для BF (`plan_engine.conditions`) и AFB (виртуальный/бумажный движок, `trade/virtual/conditions.py`), как и у остальных операторов.
- **Перегенерировано**: `python/afb_bf_protocol/schemas/` (мирроринг), `python/afb_bf_protocol/models_generated.py`, `ts/src/models.ts` (новый `ConditionNode6`/`DealV2ConditionNode6` и т.п.). `taxonomy.py`/`docs/MESSAGES.md`/`capabilities.py` не изменились — набор типов сообщений не тронут.
- **Версии**: bump до `2.0.9` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`.

## v2.0.8 — 2026-07-21

PATCH: `link.list` optional `scope` (`usable`|`admin`) to separate widget working accounts from manager admin inventory; drop `allowed_roles` from link admin / connector record. Wire AFB↔BF не затронут.

- **`link.channel.v1.json` `listRequest`** — optional `scope` (default `usable`): working ACL set vs full manager inventory.
- **`link.admin.v1.json` / `connector.record.v1.json`** — removed `allowed_roles`; ACL is `allowed_users` only.
- **Версии**: bump до `2.0.8`.

## v2.0.7 — 2026-07-21

PATCH: cleanup link connector fields — drop `display_name`, shared `setInputShared` for user/admin, optional `description`. Wire AFB↔BF не затронут.

- **`spec/schemas/afbws/bf_registry_entry.v1.json`** — убран `display_name` (больше не required).
- **`spec/schemas/afbws/link.user.v1.json`** — опциональный `description` в `sharedFields`; новый `$defs/setInputShared` (`bf_id`, `name`, `enabled`, `description`, `dry_run`, `execution_policy`); user `setInput` = `allOf` shared + `required: [bf_id]` + `unevaluatedProperties: false`.
- **`spec/schemas/afbws/link.admin.v1.json`** — admin `setInput` = `allOf` `setInputShared` + admin-extras (`broker`, `protocol`, `margin_trading`, ACL); без `display_name`.
- **Генератор**: `setInputShared` → `LinkSetInputShared` в TS/Python models.
- **Версии**: bump до `2.0.7`.

## v2.0.6 — 2026-07-21

PATCH: link health metadata (heartbeat freshness) + AFB-only informer-safe `notification.link.v1` for BF connectivity/runtime incidents/recoveries. Wire AFB↔BF не затронут.

- **`spec/schemas/afbws/link.status.v1.json`** — добавлены AFB-only поля `last_heartbeat_at`, `heartbeat_interval_sec`, `heartbeat_stale` для корректного badge/tooltip рендеринга и stale-детектации в AFB.
- **Новая схема** `spec/schemas/notification.link.v1.json` (`afb.notification.link.v1`) — MQTT-уведомление информера (Telegram/email) для событий: `link.disconnected`, `link.recovered`, `broker.degraded`/`broker.recovered`, `daemon.suspended`/`daemon.recovered`.
- **Examples**: `examples/notifications/link.degrade.json`, `link.disconnect.json`, `link.recover.json`.
- **Валидация/генерация**:
  - `python/afb_bf_protocol/payload_validation.py` + unit tests: поддержка `afb.notification.link.v1`.
  - `ts/tools/generate-models.mjs`: добавлен мэппинг `notification.link.v1.json` → `NotificationLinkV1`.
  - Перегенерированы `python/afb_bf_protocol/models_generated.py` и `ts/src/models.ts`.
- **Версии**: bump до `2.0.6` в `package.json`, `python/pyproject.toml`, `python/afb_bf_protocol/version.py`, `spec/asyncapi.yaml`.

## v2.0.5 — 2026-07-20

PATCH: план `gp-channel-migration`, протокол-часть — строгий канонический `afb.gp.v1` (графические примитивы графика) и schema-first канал `afbws.gp.channel.v1`, замена legacy bulk `settings/get_primitives`+`set_primitives`. AFB-only расширение вне `spec/asyncapi.yaml`, wire `afb.execution.v1` не тронут, BF не затронут. Backend/frontend-реализация — отдельные этапы плана, ещё не начаты.

- **`spec/schemas/gp.v1.json`** — продвигает запаркованный `spec/schemas/draft/primitive.v1.json` (удалён) в строгую сущность: обязательные `schema`/`id`/`ticker`/`kind`/`start`, `additionalProperties: false`. `ticker` — явное поле (раньше был ключом словаря `settings.primitives[secid][]`, у самого примитива его не было) — нужен для плоских `get(id)`/`list(ticker)`. Условные правила через `allOf`+`if/then/else`: `stop` обязателен для `zone`/`ruler`, запрещён для остальных; `text` (≤160 симв.) допустим только для `note`, для всех прочих — запрещён. `used_in_tradeplans` отсутствует и отвергается `additionalProperties: false` — это вычисляемые backend-данные, никогда не часть wire-сущности.
- **`spec/schemas/afbws/gp.channel.v1.json`** (`x-afbws-support-id: afbws.gp.channel.v1`) — тот же CRUD-набор, что у `alarm`: `get(id)`, `list()`/`list(ticker)`, `set(item)` (upsert по глобально уникальному `id` — перемещение примитива это обычный `set`, отдельной `move`-команды нет), `delete(id)`. Никаких bulk-set/usage/confirm команд — backend сам решает допустимость delete/move и отвечает типизированной ошибкой. `afbws.gp.error.response.v1.code` — закрытый `common.v1.json#/$defs/errorCode` (как у alarm/tradeplan, в отличие от открытого `link`-кода — существующий словарь `not_found`/`validation_error`/`conflict`/... уже покрывает нужды gp, расширять не потребовалось); `details` — новый `$defs/errorDetails` (`tradeplan_ids`, `deal_ids`, `locked_scopes`), заполняется только при `conflict`.
- `ts/tools/generate-models.mjs`: `namedRootSchemas()`/`NAMED_DEF_SCHEMAS` расширены именами новых типов (`GpV1`, `GpChannelV1Message`, `GpGetRequest`/`Response`, `GpListRequest`/`Response`, `GpSetRequest`/`Response`, `GpDeleteRequest`/`Response`, `GpErrorResponse`, `GpErrorDetails`); capability-константа `GP_CHANNEL_V1` — из `x-afbws-support-id`, экспортирована из `afb_bf_protocol/__init__.py` и TS `index.ts`. Известное ограничение генератора: `allOf`+`if/then/else` в `gp.v1.json` даёт TS-типу `GpV1` защитную `[k: string]: unknown` (json-schema-to-typescript не умеет точно вывести условные ветки в тип) — Python `TypedDict` (`models_generated.py`) сгенерирован точно, без этой особенности; фактическая строгая валидация на обеих сторонах не зависит от точности TS-типа.
- Legacy `settings/primitive.v1.json`/`settings/messages.v1.json` (запаркованы в `draft/`, шаблонизация settings заморожена) не трогали и не восстанавливали.
- PATCH: только новая `gp.v1.json` + `afbws/gp.channel.v1.json` и генератор; `spec/asyncapi.yaml` (кроме версии) и существующие канонические схемы не менялись. Тег не поставлен, пины потребителей (AFB/BF) не обновлены — по решению пользователя это отдельный шаг после ревью протокольной части.

## v2.0.4 — 2026-07-20

PATCH: план `link-channel-migration`, Фаза 1 (протокол) — schema-first канал `link` для управления и мониторинга BF-коннекторов, заменяющий legacy `connector`/`bfs`. AFB-only расширение вне `spec/asyncapi.yaml`, wire `afb.execution.v1` не тронут, BF не затронут.

- **`spec/schemas/afbws/link.user.v1.json`** — non-manager view конфигурации коннектора на общей базе `bf_registry_entry.v1.json` (как и `connector.record.v1.json`). Общие поля (`dry_run`, `margin_trading`, `execution_policy`, `paired`, `pairing_pending`, `pairing_expires_at`, `kind`, `editable`) объявлены один раз в `$defs/sharedFields` и переиспользуются `link.admin.v1.json` через `$ref`, а не дублируются — так две view-схемы не могут «разъехаться» независимо. `unevaluatedProperties: false` поверх `allOf`, а не дублирование `additionalProperties` по каждой ветке. Синтетический `virtual` — обычный экземпляр этой схемы с `kind: "virtual"`. Отдельный `$defs/setInput` — только `bf_id`/`dry_run`/`execution_policy`.
- **`spec/schemas/afbws/link.admin.v1.json`** — manager view: `$ref` на `link.user.v1.json#/$defs/sharedFields` + `allowed_roles`/`allowed_users`/`public_key_id`/`public_key_file`. Свой `$defs/setInput` — create/update набор (`bf_id` опущен → create). Ни один из view не несёт `connected`/`daemon`/session runtime — это отдельная `link.status.v1.json`. Никакого отдельного `link.common.v1.json` — общих `$defs`, которые требовали бы жёсткого перечисления, не заводили: `kind` — обычный inline-enum в `sharedFields`, коды ошибок ниже.
- **`spec/schemas/afbws/link.status.v1.json`** — runtime-only статус: `bf_id`, `connected`, `updated_at`, `daemon` (`null` либо `$ref` на `payloads/daemon.status.json`), `session` (`null` либо `account_id`+эффективный `dry_run`+`capabilities` — только то, что уже реально отдаёт `ExecutionService.accessible_bfs_map` сегодня; без надуманной `dry_run_afb`/`dry_run_bf`/`margin_trading*`-детализации — ни один из вариантов не используется и не планируется).
- **`spec/schemas/afbws/link.channel.v1.json`** (`x-afbws-support-id: afbws.link.channel.v1`) — `get`/`list` (без фильтров)/`set`/`delete` плюс отдельные `pair`/`restart` (оба требуют явный `id`, `restart` никогда не выбирает первый BF неявно); `setRequest.item` — `anyOf` (не `oneOf`: user- и admin-формы `setInput` не эксклюзивны структурно — ни одна не несёт дискриминирующего `schema`, `oneOf` ошибочно отклонял бы валидный минимальный payload как неоднозначный); типизированные ошибки `afbws.link.error.response.v1` — `code` открытая строка (`minLength: 1`), без строгого enum: жёсткая проверка вокабуляра не нужна, её обеспечивает бэкенд, а не схема; отдельные push `afbws.link.sync.push.v1` (конфиг), `afbws.link.status.sync.push.v1` (начальный снимок статусов) и `afbws.link.status.push.v1` (один изменившийся статус) — конфиг и статус никогда не смешиваются в одном push.
- Никаких полей `pairable`/`restartable` в user/admin view — избыточны рядом с явными `pair`/`restart` RPC, убраны на этапе ревью.
- Legacy `connector.*`/`bfs.registry.v1.json` не изменены и не удалены — deprecated-fallback до отдельной задачи по факту эксплуатации.
- `ts/tools/generate-models.mjs`: `namedRootSchemas()`/`NAMED_DEF_SCHEMAS` расширены именами новых типов (`LinkUserV1`, `LinkAdminV1`, `LinkStatusV1`, `LinkSharedFields`, `LinkEntity`, `LinkSetInput`, `LinkGetRequest`, `LinkSyncPush`, `LinkStatusPush` и т.д.); capability-константа `LINK_CHANNEL_V1` — из `x-afbws-support-id`, экспортирована из `afb_bf_protocol/__init__.py` и TS `index.ts`.
- PATCH: только новые `afbws/`-схемы и генератор; `spec/asyncapi.yaml` (кроме версии) и существующие канонические схемы не менялись.

## v2.0.3 — 2026-07-20

PATCH: Фаза 1 плана `entity-ws-migration` — канон и capability handshake для новых schema-first каналов `alarm`/`tradeplan` (frontend↔AFB-бэкенд, не пересекает AFB↔BF; BF не затронут и не обновляется).

- **`spec/schemas/afbws/common.v1.json`** — общие $defs: `requestId`, `errorCode`.
- **`spec/schemas/afbws/alarm.channel.v1.json`** (`x-afbws-support-id: afbws.alarm.channel.v1`) — get/list/set/delete request/response, typed `error.response`, `triggered.push` (замена `mail/alarms`) и `ack.request`/`ack.response` (замена `mail/ack`). Домен — существующий `afb.alarm.v1`, без изменений.
- **`spec/schemas/afbws/tradeplan.channel.v1.json`** (`x-afbws-support-id: afbws.tradeplan.channel.v1`) — get/list/set/delete, typed `error.response` (несёт `item` при конфликте delete), `sync.push` (замена `mail/plans`). `entity` — union `afb.tradeplan.v1`/`afb.tradeplan.v2`; v1 обёрнут `allOf` с обязательным `schema` (в каноне `tradeplan.v1.json` он опционален ради legacy-совместимости — здесь ужесточён только для нового канала). `amend_results[]` — новый `afbws.tradeplan.amend_result.v1`.
- Все сообщения новых каналов: обязательные `channel`+`schema` (`type` запрещён — маршрутизация только по ним), `additionalProperties: false`, request/response дополнительно требуют `request_id`; push-сообщения (`triggered.push`, `sync.push`) его не несут.
- **Capability-id константы**: новый генератор `collect_afbws_capability_ids()`/`render_capabilities()`/`render_capabilities_ts()` в `tools/generate.py` — сканирует `x-afbws-support-id` во всех `spec/schemas/afbws/*.json` и пишет `python/afb_bf_protocol/capabilities.py` + `ts/src/capabilities.ts` (реэкспортирован из `ts/src/index.ts`). Не смешивается с AsyncAPI `taxonomy.py`/`taxonomy.ts` (AFB↔BF).
- `ts/tools/generate-models.mjs`: `namedRootSchemas()`/`NAMED_DEF_SCHEMAS` расширены именами новых message-типов (`AlarmGetRequest`, `AlarmTriggeredPush`, `TradeplanEntity`, `TradeplanSyncPush` и т.д.).
- PATCH: только новые `afbws/`-схемы и генераторы; `spec/asyncapi.yaml` (кроме версии) и существующие `spec/schemas/*.json` канон не менялись.

## v2.0.1 — 2026-07-19

> **Note:** тег `v2.0.2` (типизация канала `settings`) отозван: схемы перенесены в
> `spec/schemas/draft/` и не входят в пакет/генерацию моделей. Актуальная версия
> пакета снова `2.0.1`.


PATCH: типизация четырёх каналов исполнения AFB↔фронтенд (`deal`, `connector`, `bfs`, `account`) — расширение вне `asyncapi.yaml`, wire `afb.execution.v1` не тронут, BF не затронут.

- **Python-типы**: новый генератор `models_generated.py` (TypedDict, `datamodel-code-generator`) — Python-зеркало `models.ts`, из того же сбандленного `spec/.generated/bundled-schema.json` (эфемерный, не коммитится), который пишет `ts/tools/generate-models.mjs`. Общие имена $defs совпадают между TS и Python. Гейтится наличием `datamodel-code-generator` (dev-dep) — при отсутствии тулзы или Node генерация тихо пропускается.
- **`spec/schemas/afbws/`** — новая конвенция (как `notification.*.v1.json`): схемы AFB-бэкенд↔AFB-фронтенд, никогда не пересекающие AFB↔BF:
  - `deal.event.v1.json`, `deal.pnl.v1.json`, `deal.record.v1.json` — три push-формата канала `deal`.
  - `bf_registry_entry.v1.json` — общий публичный минимум записи BF-коннектора (основа для `connector`/`bfs`).
  - `connector.record.v1.json`, `connector.list.v1.json` — записи канала `connector` (owner/manager-поля — опциональные, различаются по фактическому наполнению, не по дискриминанту).
  - `bfs.registry.v1.json` — push `registry` канала `bfs` (расширяет `bf_registry_entry.v1.json` рантайм-полями).
  - `account.snapshot.v1.json`, `account.orders.v1.json`, `account.catalog.v1.json`, `account.instrument.v1.json`, `account.events.v1.json` — фронтенд-вид канала `account`; `data` в первых четырёх намеренно оставлен как открытый объект (`additionalProperties: true`) — BF-payload там не схематизирован ни в одном другом месте, конвертировать в строгую форму значило бы придумывать несуществующий контракт.
- `ts/tools/generate-models.mjs`: `namedRootSchemas()`/`NAMED_DEF_SCHEMAS` расширены записями `afbws/*` для чистых имён экспортов (`DealEventPush`, `ConnectorRecord`, `BfsRegistryEntry`, `AccountSnapshotPush` и т.д.).
- `AFB/docs/API_TYPES_REGISTRY.md` — реестр типизации обновлён, все 4 канала помечены ✅/🚧 по факту миграции.
- PATCH: только новые `afbws/`-схемы и генератор, ничего в `spec/asyncapi.yaml`/`spec/schemas/*.json` (канон) не менялось.

## v2.0.0 — 2026-07-18

MAJOR (разрешение пользователя получено): репозиторий начинает поставлять сгенерированный TypeScript-пакет наравне с Python — `npm i github:Rolo837/AFB-BF-protocol#v2.0.0`, никакой публикации в npm registry. Версия провода `afb.execution.v1` не меняется — AFB и BF обновляются согласованно (правило «одна MAJOR»).

- **`ts/`** — новый TS-пакет: корневой `package.json` (`exports: ".", "./taxonomy", "./models"`), сгенерированные `ts/src/taxonomy.ts` (зеркало `taxonomy.py`) и `ts/src/models.ts` (домейн-модели из `spec/schemas/**/*.json` — `ts/tools/generate-models.mjs` бандлит все схемы в один граф `$defs` с детерминированными именами, так что общий поддефайн вроде `condition.v1.json`'s `priceExpr` объявляется один раз и переиспользуется во всех потребителях, а не дублируется). Всё генерируется через `afb-bf-protocol-generate` (Node — опциональная зависимость только для `models.ts`).
- MAJOR-содержимое — breaking-чистка из v1.16.0 (см. ниже): удалены `quoteExpr`, deprecated tick-операторы, `entry.order`, legacy `entry.side`, расширенный словарь `tradeplan.v1.direction`.
- Версия в **четырёх** файлах репозитория: `python/pyproject.toml`, `version.py`, `spec/asyncapi.yaml`, `package.json`. Пины потребителей — **пять** мест (+ `AFB/frontend/package.json`).

## v1.16.0 — 2026-07-18

Подготовительная чистка перед v2.0.0 (TypeScript-пакет): удаление deprecated-словаря условий и legacy-полей, исполняющее пометки «removal planned for v2.0.0», проставленные с v1.4.0/v1.11.0.

- **`condition.v1.json`**: удалены `quoteExpr` (`source: "quote"`) и `deprecatedTickScalarOp` (тиковые `crosses_above`/`crosses_below`/`crossing` на price без `timeframe`). Price-условия теперь поддерживают четыре оператора: `touch`, `above`/`below` (уровень), `breakout`/`breakdown`/`crossing` (свеча, требует `timeframe`). Indicator/dataset `scalarOp` (включая `crosses_above`/`crosses_below`/`crossing`) не затронут.
- **`deal.v1.json` / `deal.v2.json` / `tradeplan.v2.json`**: удалено `entry.order` (deprecated с v1.11.0, BF всегда игнорировал) и связанный `$defs.order`.
- **`deal.v1.json`**: удалены legacy `entry.side` (buy/sell) и корневой `anyOf`, допускавший `direction` опциональным — `direction` (long/short) теперь обязателен, единственный источник истины позиции.
- **`tradeplan.v1.json`**: `direction` сужен с переходного `["buy","long","sell","short"]` до `["long","short"]`.
- **`payloads/deal.accepted.json`**: удалено `entry_order_type` (deprecated с v1.11.0).
- `condition_semantics.py`, `amend_rules.py` — синхронизированы с канoном; убраны константы `DEPRECATED_PRICE_TICK_OPS`, `DEPRECATED_PRICE_OPS`, `DEPRECATED_QUOTE_OPS`.
- PATCH: только удаление уже помеченных deprecated-веток на согласованных с BF/AFB потребителях; версия провода не меняется. Формально удаление принимаемых полей несовместимо, но релиз выпускается как промежуточный шаг перед v2.0.0 осознанно (решение пользователя) — AFB и BF деплоятся согласованно.

## v1.14.1 — 2026-07-17

Опциональное поле `connector` на шаблонах торгового плана (AFB-side, не пересекает канал AFB↔BF).

- `tradeplan.v1.json` / `tradeplan.v2.json`: `connector` — непустая строка `bf_id` (реальный коннектор или `virtual`); отсутствует, если у пользователя нет capability `trade`/`virtual`.
- PATCH: расширение схем, не входящих в AsyncAPI wire.

## v1.14.0 — 2026-07-16

Уведомления о сделках в информер (MQTT `afb/deals/<user_id>`) + прокидывание времени события BF на провод.

- **Новая схема** `notification.deal.v1.json` (`afb.notification.deal.v1`) — MQTT-уведомление о сделке (триггер условия, выставление/исполнение ордера, изменение позиции, закрытие с фин. результатом) для демона informer. Не входит в AsyncAPI, не пересекает канал AFB↔BF — как и alarm-уведомления.
- **Переименование** `notification.alarm_triggered.v1.json` → `notification.alarm.v1.json` (`afb.notification.alarm_triggered.v1` → `afb.notification.alarm.v1`); состав полей не изменился. Это внутреннее переименование notification-схемы AFB (не пересекает канал AFB↔BF) — по новым правилам версионирования (см. `VERSIONING.md §2`) такие изменения относятся к PATCH-уровню.
- **MINOR-часть релиза**: опциональное поле `at` (ISO-время события, из журнала BF) добавлено в wire-схемы `spec/schemas/payloads/` (`condition.triggered`, `order.created`, `order.filled`, `deal.accepted`, `deal.rejected`, `deal.status_changed`, `deal.archived`, `deal.positions_synced`, `position.opened`, `deal.report`) — обратносовместимое добавление для существующих BF.
- **Правила версионирования ужесточены**: MAJOR запрещён без специальной команды пользователя; см. `CLAUDE.md`/`VERSIONING.md §2`.
- Примеры `examples/notifications/alarm_triggered.*.json` переименованы в `alarm.*.json`; добавлены `deal.order_executed.json`, `deal.close.json`.

## v1.13.3 — 2026-07-15

Уточнение семантики защитного времени (`duration`) для price `above`/`below`: BF измеряет реальные непрерывные секунды по monotonic clock (не счётчик monitor-тиков). Прогресс сбрасывается при `false`, gap'ах оценки, amend/pause/cancel и рестарте BF; не персистится. На проводе producer обязан отправлять `above`/`below` (UI `touch` преобразуется до компиляции); multi-leg с независимым `duration` на каждый leg разрешён протоколом.

- `condition.v1.json`: описание `$defs/duration` и ветки price level.
- `PROTOCOL.md` §12: формулировка «реальные непрерывные секунды».
- Регрессионные fixtures/тесты с `duration` на stop/entry.
- PATCH: только доки/описание/тесты существующего поля; версия провода не меняется.

## v1.13.2 — 2026-07-15

Фикс отображения условия аларма в MQTT `display.condition_text`: вместо «Выше, Ордера/delta 10000» — естественная фраза «Ордера/delta выше 10000» (субъект + оператор + правая часть).

- `alarm_display.condition_text` / `build_display`: шаблон `{subject} {op.lower()} {rhs}` для price / dataset / indicator.
- Примеры `examples/notifications/alarm_triggered.*.json` обновлены.
- PATCH: только текст `display`, схема и версия провода не меняются.

## v1.13.1 — 2026-07-14

Фикс: `tradeplan.v2.json` — черновая схема торгового плана — не была обновлена вместе с v1.13.0 и держала собственный локальный enum оператора `op` (не через `condition.v1.json`), из-за чего `op: "touch"` отклонялся с `deal_id`/`entries/0/condition/op` ошибкой при сохранении плана с явным касанием.

- `tradeplan.v2.json`: `"touch"` добавлен в enum `op` общего `$defs/tpConditionNode` (используется и для входа, и для стоп/тейк-легов через `$defs/tpExitList`); уточнено описание — цена всегда несёт явный `op`, `op` опущен принимается только для старых планов.
- Новый тест `test_v2_condition_op_accepts_all_six_price_ops_and_omitted` в `test_tradeplan_schema.py`.
- PATCH: довершает обратно совместимое изменение v1.13.0, версия провода не меняется.

## v1.13.0 — 2026-07-14

Явный оператор `touch` для price-условий — шестой полноценный оператор словаря `condition.v1.json`, наравне с `above`/`below`/`breakout`/`breakdown`/`crossing`. Раньше касание кодировалось только отсутствием `op`; теперь AFB всегда шлёт `op: "touch"` явно, а чтение без `op` остаётся валидным ради обратной совместимости со старыми сделками/планами.

- `condition.v1.json`: ветка «price touch» переименована из «price touch (legacy)», принимает `op` отсутствующим или равным `"touch"`; `alarm.v1.json` получил ту же правку и заодно отделил `price level operator` (`above`/`below`) от `price tick operator (deprecated)` (только `crosses_*`/тиковый `crossing`) — раньше они были ошибочно объединены под одним deprecated-заголовком.
- `condition_semantics.py`: новая константа `PRICE_TOUCH_OPS = {"touch"}`, добавлена в `OPS_BY_SOURCE["price"]`; docstring'и операторов дополнены исполнительной семантикой на стороне BF — `touch` исполняется лимитной заявкой, остальные пять price-операторов (`above`/`below`/`breakout`/`breakdown`/`crossing`) — рыночной.
- Никакой из шести price-операторов не считается deprecated/legacy — деприкейт остаётся только у тиковых `crosses_*`/`crossing` без `timeframe` и у `quote`-условий (`bid`/`ask`), как и раньше.
- MINOR: обратно совместимо (новое опциональное явное значение `op`), версия провода не меняется.

## v1.12.0 — 2026-07-14

Enrollment: пользовательская привязка ключей BF ↔ AFB поверх `ws://` без TLS (одноразовый пейринг-токен + HMAC-подтверждение обеих сторон), взамен ручного копирования ключей админом.

- Новые сообщения: `session.enroll_request` (bf2afb, self-signed proof-of-possession), `session.enroll_response` (afb2bf, подписан боевым ключом AFB), `session.reenroll_request` (afb2bf, инициирует перепривязку/ротацию).
- Новый модуль `afb_bf_protocol.enrollment`: генерация/парсинг пейринг-токена и строки привязки (`afbpair1_…`), вывод MAC-ключа, MAC для запроса/ответа, сравнение через `hmac.compare_digest`.
- `afb_bf_protocol.signing.key_fingerprint(pub)` — отпечаток ключа (первые 12 hex `sha256(SPKI DER)`), новый источник истины для `signature.key_id`; поля `keys.public_key_id` (BF) и `afb.key_id` (AFB) деприкируются в пользу вычисляемого отпечатка.
- MINOR: обратно совместимо, версия провода не меняется.

## v1.11.0 — 2026-07-13

Устранение диктата параметров ордера со стороны AFB — тип ордера, `time_in_force` и офсет лимитника теперь целиком решает BF, исходя из возможностей своего брокерского адаптера, а не из того, что прислала сделка.

- `deal.v1`/`deal.v2` `entry.order` и одноимённый леговый `order` в `tradeplan.v2` помечены `deprecated: true` (не удалены — старые сохранённые сделки и планы продолжают проходить валидацию).
- `deal.accepted.validation.entry_order_type` помечен `deprecated: true` — BF больше не эхо́ит запрошенный тип ордера.
- `daemon.capabilities.time_in_force` теперь строгий enum `["day", "gtc", "ioc"]` (домен вместо произвольной строки); `ioc` добавлен для брокеров без поля time_in_force в API (например, REST-API Finam Arena — исключительно рыночные заявки).
- `amend_rules._entry_triggers`: семантическое поле `entry` в матрице допустимости правок сузилось до `condition` — устаревший `order`-блок в сторедже больше не может вызвать ложное «entry изменилось» при amend.
- MINOR: обратно совместимо, физическое удаление поля — в будущем MAJOR-релизе.

## v1.10.0 — 2026-07-12

- `session.hello` получил опциональный `margin_trading`; `session.hello_ack` — `margin_trading`/`margin_trading_afb`/`margin_trading_bf`, по аналогии с уже существующей тройкой `dry_run`-полей. Позволяет AFB переопределять режим маржинальной торговли BF-коннектора на сессию, не переписывая YAML-конфиг BF.
- Задокументировано фактическое поле `accepted_protocol` в `hello_ack` (схема раньше перечисляла только `protocol`).

## v1.9.0 — 2026-07-10

- Новое событие `broker.position_ledger` (bf→afb, unsolicited push, по аналогии с `broker.account`/`broker.orders`): экспонирует AFB долгоживущий леджер объёма на уровне символа, не привязанного ни к одной конкретной сделке (излишек/внешнее закрытие). Заменяет прежний подход BF с пометкой отдельных сделок как orphaned при position_mismatch — теперь это symbol-level reconcile.

## v1.8.0 — 2026-07-09 *(коммит есть в истории, git-тег не создавался)*

- Опциональные поля в `execution_policy` (общий `executionPolicy`-def `deal.v1`/`deal.v2`): `execution_mode` (`client`/`hybrid`/`server`, `server` зарезервирован) и `backstop`-оверрайды (`offset_steps`, `stop_price`, `max_loss_steps`, `take_profit` зарезервирован).
- `deal_state.v2` `order` получил роль `backstop`, статусы `watching`/`expired`, поля `stop_price`/`broker_order_id`.
- `daemon.capabilities` получил `features.execution_modes`.
- Основа для гибридной серверной SLTP-защиты (см. `BF/docs/RESILIENCE.md`, Фаза 3). Все изменения опциональны/аддитивны — MINOR.

## v1.7.2 — 2026-07-07

- Новая схема `afb.notification.alarm_triggered.v1` для MQTT-уведомлений информера — payload с уже отрендеренными строками отображения, `validate_notification()`, примеры.

## v1.7.1 — 2026-07-07

Технический повторный тег на тот же коммит, что и `v1.7.0` — изменений в содержимом нет.

## v1.7.0 — 2026-07-07

- BF Фаза 2 (эскалация/алертинг): `session.heartbeat` получил опциональный `health` (overall + points), `daemon.status` — опциональные `severity`/`health`/`changes`; `daemon_status` помечен как persisted, чтобы переходы автоматически попадали в event journal BF.

## v1.6.0 — 2026-07-07

- Формализованы включающие (inclusive) операторы цены above/below, опциональная BF-only `duration` для условий, обязательное поле `field` для dataset-условий; убрано поле `price` из wire-формы условия.

## v1.5.0 — 2026-07-06

- Задокументирован `timeframe`, который AFB уже отправлял на indicator-ветках `conditionNode.op` (раньше проходил только через открытые `additionalProperties`).
- `deal.accepted.broker_sizing` получил `estimated: boolean` для превью indicator-based sizing.
- `daemon.capabilities.market_data.timeframes` — чтобы AFB мог валидировать таймфреймы условий против того, что реально поддерживает конкретный экземпляр BF.

## v1.4.0 — 2026-07-05

- Общий словарь условий вынесен в отдельную схему `condition.v1.json` (price/quote/indicator/dataset expressions, 5 операторов сравнения) — теперь на неё ссылаются `deal.v2`, `tradeplan.v2` и новая `afb.alarm.v1`.
- Цена получила `touch` (без `op` — уровень пересечён между prev/cur) и свечные операторы (`breakout`/`breakdown`/`crossing`, оцениваются только на последней закрытой свече нужного таймфрейма); legacy тиковые price/quote операторы оставлены, но помечены deprecated (удаление планировалось на v2.0.0).
- `condition_semantics.py` стал единственным эталонным вычислителем условий (`evaluate_touch`/`evaluate_scalar_op`/`evaluate_candle_op`) для всех трёх потребителей (алармы, торговые планы, сделки); заодно исправлен подтверждённый пограничный баг пропуска crossing, начинающегося ровно с `prev == ref`.
- Новая `afb.alarm.v1.json` заменяет плоскую legacy-форму алармов AFB (`condition_type`/`trigger_type`/`value_type`/`value`/`value_ref`, `break_up`/`break_down`) тем же `conditionNode`; маппинг legacy→v1 — `docs/PROTOCOL.md` §11.

## v1.3.1 — 2026-07-02

- Косметическая перестановка полей в `afb.tradeplan.v1`/`v2` (id, ticker, status, direction, schema, ...) для читаемости — без изменений валидации или wire-поведения.

## v1.3.0 — 2026-07-02

База для торговых планов и сделок схемы v2:

- `deal.v1`: `conditionNode.left` ограничен `price/last` (было `price/quote/indicator/dataset`).
- `deal.v2`: собственный `conditionNode` (больше не `$ref` на v1) — матрица пар left/right (price/quote — только const, indicator/dataset — const или выражение того же рода).
- `deal.v2`/`tradeplan.v2`: убрано поле `side` у элементов `entry`/`entries` (список независимых buy/sell-плечей не имеет смысла для одной сделки); добавлено обязательное деал-уровневое `direction: long|short`.
- `deal.v1`/`tradeplan.v1`: переходная поддержка обоих словарей направления — `entry.side` (buy/sell) опционален при наличии корневого `direction` (long/short); `tradeplan.v1.direction` принимает `buy`/`long`/`sell`/`short`.
- Новые схемы `afb.tradeplan.v1`/`v2` (AFB-сторонние, не сообщения протокола) — формализация текущего формата торгового плана и целевого формата v2.
- Схемы упакованы в `afb_bf_protocol/schemas/` (генерируются из `spec/schemas/`) и валидируются в рантайме новым модулем `payload_validation` (`validate_deal`, `validate_tradeplan`) под extra `[validation]`.

## v1.2.0 — 2026-07-01

- `deal.snapshot` (reconcile-снимок bf→afb) теперь несёт не только агрегат `observed.position.{qty,avg_price}`, но и полный список набранных позиций `positions[]` (`{symbol, quantity, average_price, updated_at}`) по каждому символу — без этого AFB после reconcile оставлял позиции пустыми, и фоновый расчёт нереализованного P&L не имел данных.
- Заодно сведены рассинхронизировавшиеся версии (asyncapi/`__version__`/pyproject) к единой `1.2.0`.

## v1.1.4 — 2026-07-01

- `session.resync_request`/`session.resync_response` задокументированы в каноническом формате `{deals: {deal_id: {revision, status, execution_phase, archived}}}`; старые поля (`deal_revisions`, `deal_statuses`, `active_deal_ids`, `deal_archived`) помечены legacy.

## v1.1.3 — 2026-07-01

- Новый тип сообщения `deal.snapshot` (bf→afb, не хранится) — снимок состояния сделки по запросу (`status`, `execution_phase`, `observed`); BF отправляет его в ответ на `deal.operation op=reconcile`.

## v1.1.2 — 2026-06-30

- Исправление: `DealState.from_dict` теперь при пустом корневом `owner_user_id` подставляет значение из вложенной структуры сделки (backfill), а не оставляет поле пустым.

## v1.1.1 — 2026-06-29

- Уточнение матрицы допустимых правок сделки: sizing больше нельзя менять после входа в позицию вообще (было — «храповик», можно только вверх). Теперь `sizing` редактируется лишь до входа (`awaiting_entry`/`entry_working`), в `holding`/`exit_working` запрещено (`reason: size_immutable_after_entry`).

## v1.1.0 — 2026-06-29

- Механизм правки уже опубликованной/активной сделки (`deal.amend`) с жёстким гейтом по фазе исполнения: `amend_rules.evaluate_amend(old, new, ctx)` — матрица «поле × фаза», единая для AFB и BF. Вход меняется только до входа в позицию; SL/TP двигаются почти всю жизнь сделки.

## v1.0.2 — 2026-06-27

- Только подъём версии пакета (PATCH); формат провода не менялся.

## v1.0.1 — 2026-06-26

- `envelope.signing_string_parts(...)` — единый источник формата строки для подписи.
- `DealState` — каноничное супермножество состояния сделки (`observed`, `to_resync_payload`) с настраиваемым провайдером времени `set_now_iso()`.

## v1.0.0 — 2026-06-26

Первый релиз: AsyncAPI-спека (`spec/asyncapi.yaml` + `spec/schemas/`), Python-пакет `afb_bf_protocol` (конверт, подпись Ed25519, таксономия сообщений), подписанные fixtures.
