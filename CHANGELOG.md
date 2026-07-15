# Changelog

История версий протокола `afb-bf-protocol` (semver-теги пакета/спеки). Версия провода (`protocol` в конверте, поле `PROTOCOL_VERSION`) на всём этом диапазоне остаётся `afb.execution.v1` — ни один из релизов ниже не был проводным breaking change. Формат уровней версий — см. `VERSIONING.md`.

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
