# Протокол взаимодействия AFB ↔ BF (afb.execution.v1)

## Обзор

**AFB** (OMS, сервер) — хранит сделки, принимает WS-подключения от BF.  
**BF** (Belphegor, исполнитель) — подключается к AFB, исполняет сделки через брокерский API.

Каждое сообщение — подписанный JSON-конверт (`spec/schemas/envelope.json`, подпись Ed25519).
Транспорт: WebSocket, BF подключается к AFB на `ws://<host>/bf/v1`.

---

## 1. Начальное рукопожатие (Handshake)

```mermaid
sequenceDiagram
    participant BF
    participant AFB

    BF->>AFB: WS connect → /bf/v1
    BF->>AFB: session.hello
    note right of BF: bf_id, protocol, nonce,<br/>version, dry_run, margin_trading

    AFB->>BF: session.hello_ack
    note left of AFB: server_nonce, heartbeat_interval_sec,<br/>protocol, dry_run, dry_run_afb, dry_run_bf,<br/>margin_trading, margin_trading_afb, margin_trading_bf

    BF->>AFB: session.resync_request
    note right of BF: deal_revisions {deal_id: revision},<br/>deal_statuses {deal_id: status},<br/>deal_archived {deal_id: reason}

    AFB->>BF: session.resync_response
    note left of AFB: deal_revisions {deal_id: revision},<br/>deal_statuses {deal_id: status}<br/>(только активные сделки)

    alt Есть сделки для отправки BF
        AFB->>BF: deal.publish  (для каждой новой/изменённой сделки)
        BF->>AFB: deal.accepted {command_type: "deal.publish", binding, broker_instrument, broker_sizing}
    end

    alt Есть сделки для синхронизации статуса
        AFB->>BF: deal.operation {operations: [{deal_id, status, revision}]}
        BF->>AFB: deal.accepted {command_type: "deal.operation"}
    end

    alt BF сообщил об архивных сделках (deal_archived)
        AFB-->>AFB: асинхронно архивирует сделки из deal_archived
    end

    loop Heartbeat (каждые heartbeat_interval_sec секунд)
        BF->>AFB: session.heartbeat {bf_id, broker_connected}
    end
```

### Детали шагов

| Шаг | Отправитель | Тип | Ключевые поля payload |
|-----|-------------|-----|-----------------------|
| 1 | BF | `session.hello` | `bf_id`, `protocol`, `nonce`, `dry_run`, `margin_trading` |
| 2 | AFB | `session.hello_ack` | `server_nonce`, `heartbeat_interval_sec`, `dry_run`, `dry_run_afb`, `dry_run_bf`, `margin_trading`, `margin_trading_afb`, `margin_trading_bf` |
| 3 | BF | `session.resync_request` | `deal_revisions`, `deal_statuses`, `deal_archived` |
| 4 | AFB | `session.resync_response` | `deal_revisions`, `deal_statuses` (только активные) |
| 5+ | AFB | `deal.publish` / `deal.operation` | при необходимости досинхронизации |

`dry_run`/`margin_trading` в `session.hello` — собственные (конфигурационные) значения BF. AFB-реестр (`trading_bf.yaml`) хранит для каждого коннектора `Optional[bool]` override: если задан — AFB замещает значение BF на всю сессию (уходит в соответствующее поле `hello_ack`); если не задан (`null`) — действует значение BF из `hello`. Ни dry_run, ни margin_trading никогда не перезаписывают yaml-конфиг BF — override живёт только в рамках текущей сессии AFB↔BF. (Начиная с v1.10.0; до этого `dry_run` в `hello_ack` был `dry_run_afb OR dry_run_bf`, а `margin_trading` на проводе отсутствовал.)

---

## 2. Resync: алгоритм выравнивания инвентаря

BF посылает `session.resync_request` после каждого переподключения.

```
deal_revisions  — {deal_id: revision}  все активные сделки на BF
deal_statuses   — {deal_id: status}    статусы активных сделок на BF
deal_archived   — {deal_id: reason}    сделки, заархивированные на BF
                                        пока не было связи с AFB
```

AFB сравнивает инвентарь BF с хранилищем и принимает решение для каждой сделки:

| Условие | Действие AFB |
|---------|--------------|
| Сделка есть на BF, нет в AFB | `none` — BF ведёт её самостоятельно |
| Ревизия и статус совпадают | `none` — синхронизировано |
| Статус отличается, ревизия совпадает | `status_sync` → `deal.operation` |
| Ревизия отличается, BF-статус `published`/`cancelled` | `publish` → `deal.publish` |
| Ревизия отличается, BF-статус активный/паузированный | `ignore_unsafe_revision` — не трогаем |
| deal_id присутствует в `deal_archived` | исключается из resync_response, архивируется на AFB |

---

## 3. Жизненный цикл сделки

```mermaid
stateDiagram-v2
    [*] --> publishing : AFB создаёт сделку
    publishing --> published : deal.accepted (deal.publish)
    publishing --> cancelled : deal.rejected

    published --> active : deal.operation activate
    published --> waiting_external_signal : deal.operation activate (внешний сигнал)
    waiting_external_signal --> active : deal.signal

    active --> paused : deal.operation pause
    paused --> active : deal.operation resume
    active --> closed : закрытие позиции
    active --> cancelled : deal.operation cancel
    paused --> cancelled : deal.operation cancel
    active --> orphaned : потеря привязки
    paused --> orphaned : потеря привязки

    closed --> [*]
    cancelled --> [*]
    orphaned --> [*]
    published --> [*] : deal.archived (no_binding)
    active --> [*] : deal.archived (instrument_delisted)
```

### Статусы

| Статус | Где | Значение |
|--------|-----|----------|
| `publishing` | AFB | сделка создана, ожидаем принятия BF |
| `published` | BF/AFB | BF принял, ждёт активации |
| `waiting_external_signal` | BF/AFB | ждёт внешнего сигнала на вход |
| `active` | BF/AFB | сделка активна, BF исполняет |
| `paused` | BF/AFB | исполнение приостановлено |
| `closed` | BF/AFB | позиция закрыта штатно |
| `cancelled` | BF/AFB | сделка отменена |
| `orphaned` | BF/AFB | потеряна брокерская привязка |

---

## 4. Команды AFB → BF и ответы BF

### 4.1 `deal.publish` — публикация сделки

**AFB → BF:**
```json
{ "deal": { /* afb.deal.v1 или afb.deal.v2 */ } }
```

**BF → AFB (успех):** `deal.accepted`
```json
{
  "command_type": "deal.publish",
  "deal_id": "deal-xxx:bf-id",
  "revision": 1,
  "binding": { "account_id": "...", "symbol": "ALRS@MISX" },
  "broker_instrument": { /* параметры инструмента от брокера */ },
  "broker_sizing": { "lots": 185, "required_cash": "4713.8", ... }
}
```

**BF → AFB (ошибка):** `deal.rejected`
```json
{
  "command_type": "deal.publish",
  "deal_id": "deal-xxx:bf-id",
  "code": "broker_grpc",
  "message": "Security not found"
}
```

---

### 4.2 `deal.operation` — операции над сделкой

**AFB → BF:**
```json
{
  "operations": [
    { "deal_id": "deal-xxx:bf-id", "op": "activate", "revision": 1 }
  ]
}
```

Допустимые `op`:

| op | Требуемый статус | Результат | Примечание |
|----|-----------------|-----------|------------|
| `activate` | `published` | `active` / `waiting_external_signal` | запускает исполнение |
| `pause` | `active` | `paused` | приостанавливает новые ордера |
| `resume` | `paused` | `active` | возобновляет |
| `cancel` | `active`, `paused` | `cancelled` | отменяет ордера и позицию |
| `reconcile` | `published`, `active`, `paused`, `orphaned` | — | пересверка с брокером |
| `delete` | `published`, `cancelled`, `closed`, `orphaned` | — | удаление с BF |
| `status` | любой | — | принудительная установка статуса (resync) |

**BF → AFB (успех):** `deal.accepted`
```json
{ "command_type": "deal.operation", "deal_id": "deal-xxx:bf-id" }
```

**BF → AFB (ошибка):** `deal.rejected`

---

### 4.3 `deal.resync` — полная пересинхронизация сделок

**AFB → BF:** массив сделок с актуальными данными и статусами.

```json
{
  "deals": [
    {
      "deal_id": "deal-xxx:bf-id",
      "revision": 3,
      "status": "active",
      "deal": { /* afb.deal.v2 */ },
      "status_history": [...],
      "source_refs": {}
    }
  ]
}
```

**BF → AFB:** `deal.accepted` с `command_type: "deal.resync"`.

---

### 4.4 `deal.signal` — внешний сигнал на вход

**AFB → BF:**
```json
{ "deal_id": "deal-xxx:bf-id" }
```

Переводит сделку из `waiting_external_signal` → `active`.  
**BF → AFB:** `deal.accepted` с `command_type: "deal.signal"`.

---

### 4.5 Broker-запросы (парные команды)

| Команда AFB → BF | Ответ BF → AFB | Описание |
|------------------|----------------|----------|
| `broker.get_account` | `broker.account` | баланс и параметры счёта |
| `broker.get_orders` | `broker.orders` | список активных ордеров |
| `broker.get_catalog` | `broker.catalog` | инструменты биржи/рынка |
| `broker.get_instrument` | `broker.instrument` | параметры конкретного инструмента |
| `broker.resolve_instrument` | `broker.instrument_resolved` | резолюция инструмента для сделки |

Все запросы используют `idempotency_key` и `correlation_id` для сопоставления ответа с запросом.

---

### 4.6 `daemon.capabilities_query` / `daemon.restart`

| Команда | Ответ | Описание |
|---------|-------|----------|
| `daemon.capabilities_query` | `daemon.capabilities` | возможности брокерского адаптера |
| `daemon.restart` | — (BF перезапускается) | перезапуск BF-демона |

---

## 5. События BF → AFB (без запроса)

### 5.1 Торговые события сделки

Все торговые события несут `deal_id`, `revision` и записываются в `trading_events` журнал BF.

| Событие | Payload | Когда |
|---------|---------|-------|
| `deal.status_changed` | `deal_id`, `status`, `revision`, `execution_phase`, `last_price` | смена статуса сделки |
| `deal.archived` | `deal_id`, `revision`, `reason`, `archived_at` | сделка удалена с BF |
| `deal.orders_synced` | `deal_id`, ордера | синхронизация списка ордеров |
| `deal.positions_synced` | `deal_id`, позиции | синхронизация позиций |
| `deal.report` | `deal_id`, итоговые данные | закрытие сделки |

Причины архивации (`deal.archived.reason`):

| reason | Что произошло |
|--------|---------------|
| `no_binding` | сделка принята BF, но брокерская привязка не установлена |
| `instrument_delisted` | инструмент исчез из брокерского каталога |
| `user_delete` | пользователь удалил сделку через AFB |

### 5.2 Торговые события ордеров и позиций

| Событие | Когда |
|---------|-------|
| `condition.triggered` | условие входа/выхода сработало |
| `order.created` | ордер выставлен брокеру |
| `order.partially_filled` | частичное исполнение |
| `order.filled` | полное исполнение |
| `order.cancelled` | ордер отменён |
| `order.rejected` | ордер отклонён брокером |
| `position.opened` | позиция открыта |
| `position.changed` | размер позиции изменился |
| `position.closed` | позиция закрыта |

### 5.3 Системные события

| Событие | Когда |
|---------|-------|
| `session.heartbeat` | каждые `heartbeat_interval_sec` секунд |
| `daemon.status` | изменение состояния BF-демона |
| `daemon.capabilities` | ответ на `daemon.capabilities_query` |
| `daemon.error` | критическая ошибка в BF |

---

## 6. Конверт и подпись

Каждое сообщение обёрнуто в стандартный конверт (`spec/schemas/envelope.json`):

```json
{
  "protocol": "afb.execution.v1",
  "message_id": "<uuid4>",
  "correlation_id": "<uuid4 | null>",
  "causation_id": "<uuid4 | null>",
  "sender": "<bf_id | afb>",
  "recipient": "<bf_id | afb>",
  "type": "<message type>",
  "created_at": "<ISO 8601>",
  "expires_at": "<ISO 8601>",
  "idempotency_key": "<string>",
  "payload_hash": "<sha256 hex>",
  "payload": { /* тип-специфичный объект */ },
  "signature": { "alg": "Ed25519", "key_id": "...", "value": "<base64url>" }
}
```

- `correlation_id` — заполняется ответчиком: берётся `message_id` запроса, к которому относится ответ.
- `idempotency_key` — гарантия at-most-once обработки на принимающей стороне.
- `payload_hash` — SHA-256 от канонической строки подписи (отдельно от конверта).

Подпись покрывает: `message_id`, `sender`, `recipient`, `type`, `created_at`, `expires_at`, `idempotency_key`, `payload_hash`.

---

## 7. Схема correlation_id для парных сообщений

```
BF           correlation_id = null
  → AFB:  session.resync_request (message_id = "AAA")

AFB          correlation_id = "AAA"  (ссылается на запрос BF)
  → BF:   session.resync_response

AFB          correlation_id = null
  → BF:   deal.publish (message_id = "BBB")

BF           correlation_id = "BBB"  (ссылается на команду AFB)
  → AFB:  deal.accepted / deal.rejected
```

---

## 8. Идемпотентность

`idempotency_key` формируется по правилу `<sender>:<type>:<uuid>`. BF дедуплицирует входящие команды и при повторной доставке отвечает кешированным ответом, не выполняя операцию снова. TTL кеша настраивается (по умолчанию 600 сек).

---

## 9. Связанные файлы

| Файл | Содержимое |
|------|-----------|
| `spec/asyncapi.yaml` | Полная AsyncAPI-спека всех сообщений |
| `docs/MESSAGES.md` | Каталог сообщений (генерируется из asyncapi.yaml) |
| `spec/schemas/envelope.json` | JSON Schema конверта |
| `spec/schemas/deal.v1.json` | Схема сделки v1 (одна точка входа/выхода) |
| `spec/schemas/deal.v2.json` | Схема сделки v2 (множество точек входа/выхода) |
| `spec/schemas/tradeplan.v1.json` | Шаблон торгового плана v1 (AFB-сторонний, см. §10) |
| `spec/schemas/tradeplan.v2.json` | Шаблон торгового плана v2 (AFB-сторонний, см. §10) |
| `spec/schemas/condition.v1.json` | Единый словарь операторов условия (см. §12) |
| `spec/schemas/alarm.v1.json` | Аларм AFB (AFB-сторонний, см. §11) |
| `spec/schemas/payloads/` | JSON Schema каждого payload |
| `examples/` | Подписанные примеры конвертов |
| `examples/tradeplans/` | Примеры шаблонов ТП (не конверты, не подписываются) |
| `examples/alarms/` | Примеры алармов (не конверты, не подписываются) |
| `python/afb_bf_protocol/` | Python-пакет: модели, подпись, валидация |
| `python/afb_bf_protocol/payload_validation.py` | Рантайм-валидация deal/tradeplan/alarm payload'ов (extra `[validation]`) |
| `python/afb_bf_protocol/condition_semantics.py` | Эталонный evaluator операторов условия (см. §12) |

---

## 10. Шаблоны торговых планов (afb.tradeplan.v1 / afb.tradeplan.v2)

Шаблон торгового плана (ТП) — **не сообщение протокола**: он не описан в
`asyncapi.yaml`, не оборачивается в конверт и никогда не идёт по каналу
AFB↔BF. Это AFB-сторонняя сущность — черновик, который пользователь
редактирует на фронтенде и хранит в своих настройках (`tradeplans` в
пользовательском YAML). Схемы `spec/schemas/tradeplan.v1.json` и
`tradeplan.v2.json` живут в этом репозитории (а не в AFB) по одной причине:
шаблон ТП напрямую и однозначно связан со схемой сделки, которую AFB из него
компилирует — контракт `compile(tradeplan.vN) → deal.vN` проверяется тестами
в обоих репозиториях.

Версия шаблона определяется полем `schema` внутри самого объекта ТП
(`"afb.tradeplan.v1"` / `"afb.tradeplan.v2"`), а **не** полем протокола нигде
на проводе. Единственное правило совместимости: если поле `schema`
отсутствует, шаблон считается `afb.tradeplan.v1` — так продолжают работать
фронтенды старее самой схемы ТП, которые никогда это поле не выставляли.

- **`afb.tradeplan.v1`** — одна точка входа, опциональные тейк/стоп; условия —
  цена (`price_value`) или ссылка на график-примитив линии (`primitive_id`).
  `direction` — поле верхнего уровня, однозначное (одна точка входа), но с
  **переходным словарём** `"buy" | "long" | "sell" | "short"`: `buy`/`sell` —
  устаревшее значение (то, что фронтенд шлёт сегодня), `long`/`short` —
  целевое (тот же словарь, что в `afb.deal.v1`/`v2` и `afb.tradeplan.v2`); оба
  принимаются, пока фронтенд не переведён на `long`/`short`. Компилируется в
  `afb.deal.v1`.
- **`afb.tradeplan.v2`** — списки `entries[]` (вход) и `stop_loss[]`/
  `take_profit[]` (выход) с `percent`, компилируется в `afb.deal.v2`. Условия
  — узлы, совместимые по форме с `conditionNode` из `deal.v2.json` (`op`
  необязателен — выводится AFB из направления/роли при компиляции), плюс
  расширение: сторона `right` может быть `primitiveRef`
  (`{"primitive_id": "..."}`) — ссылка на горизонтальную линию, которую AFB
  разрешает в decimal-константу при компиляции по тому же механизму
  снапшотов, что и в v1. `sizing` в шаблоне v2 уже в deal-формате
  (`{mode, value}` с decimal-строками), а не в старом `quantity_mode`/
  `quantity_value` — учитывать при переводе фронтенда на v2.

**`direction` (long/short) в v2 — обязательное поле верхнего уровня**, единый
источник направления позиции для всей сделки/плана. У элементов списка
`entries[]` (как и `deal.v2.json`) **нет поля `side`** — список из независимых
buy/sell-плечей не имеет определённой семантики для одной сделки («50% buy,
50% sell» — это не одна позиция). Брокерская сторона (buy/sell) каждого плеча
выводится AFB/BF из `direction` и роли плеча: `long`-вход и `short`-выход —
buy; `short`-вход и `long`-выход — sell.

`afb.deal.v1` (сама схема сделки, не только шаблон) тоже получила
опциональное корневое поле `direction` (long/short) как альтернативу
устаревшему `entry.side` (buy/sell): деал обязан иметь **хотя бы одно** из
двух (`anyOf` в `deal.v1.json`), допустимо и оба сразу. Бэкенд AFB переходит
на `direction` как источник истины, но при компиляции продолжает
проставлять и `entry.side` — ради BF и любого другого кода, который ещё
читает только его; `entry.side`, если присутствует, имеет приоритет при
определении «сторона изменилась» в `amend_rules._sides`.

Важно: `tradeplan.v2.json` **намеренно не enforce-ит** полную матрицу
допустимых пар `left`/`right` (price/quote — только `const`; indicator/
dataset — `const` или выражение того же вида), которую определяет
`deal.v2.json` — из-за `primitiveRef` в `right` комбинаторика взорвалась бы.
Эту матрицу проверяют уже после компиляции: JSON Schema `deal.v2.json`
(структурно) и BF (по сути, `validate_condition_node`).

Валидация обеих схем на рантайме — `afb_bf_protocol.payload_validation`
(`validate_tradeplan`, `validate_deal`; extra `pip install
afb-bf-protocol[validation]`). BF эту зависимость не ставит — шаблоны ТП его
не касаются.

## 11. Алармы (afb.alarm.v1)

Аларм, как и шаблон ТП, — **не сообщение протокола**: не описан в
`asyncapi.yaml`, не оборачивается в конверт, никогда не идёт по каналу
AFB↔BF. Это AFB-сторонняя сущность (пользовательские оповещения),
`spec/schemas/alarm.v1.json` живёт в этом репозитории по той же причине, что и
`tradeplan.v2.json` — общий словарь операторов условий с `deal.v2`/
`tradeplan.v2` (см. §12).

`afb.alarm.v1` заменяет легаси-формат YAML-аларма AFB (плоские поля
`condition_type`/`trigger_type`/`value_type`/`value`/`value_ref`, имена
операторов `break_up`/`break_down`) на `conditionNode`, совместимый по форме с
`condition.v1.json`, с одним отличием: индикаторное выражение (`left`/`right`
с `source: indicator`) требует только `source`+`id` — тип/параметры индикатора
AFB резолвит из сохранённых настроек пользователя по `id`, они не едут в самом
условии аларма (`deal.v2`/`tradeplan.v2`, наоборот, несут `type`/`params`
инлайн).

Top-level `period` — общий таймфрейм вычисления аларма (легаси-дефолт
`10min`); когда `condition` — свечной ценовой оператор, `condition.timeframe`
несёт таймфрейм свечи и по построению равен `period`.

Легаси-алармы читаются конвертером (ленивая миграция: конверсия при чтении,
перезапись в новом формате при сохранении/переактивации — инициируется
фронтендом AFB). Таблица маппинга легаси → v1:

| Легаси (`condition_type` + `trigger_type`/`value_type`) | `afb.alarm.v1` |
|---|---|
| `price` без `trigger_type` | `left: {source: price, field: last}`, `right: {const: value}`, **без `op`** (касание) |
| `price` + `above`/`below` | `op: above`/`below` — deprecated-тиковая ветка **без переименования**: сохраняет легаси-семантику уровня (аларм с ценой уже за уровнем срабатывает сразу; касание при создании «за уровнем» не сработало бы). Из UI не предлагается; при редактировании пересохраняется как касание |
| `price` + `break_up`/`break_down` | `op: breakout`/`breakdown`, `timeframe = period` аларма |
| `price` + `crossing` | `op: crossing`, `timeframe = period` аларма (свечной; у легаси-аларма `period` есть всегда, дефолт `10min`) |
| `indicator` + `break_up`/`break_down` | `op: crosses_above`/`crosses_below` |
| `indicator` + `above`/`below`/`crossing` | без переименования |
| `volume` (`condition_type=volume`) | `left: {source: dataset, dataset_id: volume}` — формат конвертируется, но **вычисление в бэкенде временно отключено** (см. §12, «volume») |
| `positions`/`orders`/`hhi`/`trades` | `left: {source: dataset, dataset_id: <тип>, field: condition_ref}` |
| `value_type=indicator`, `value_ref` | `right: {source: indicator, id: value_ref}` |
| `value_type=value`, `value` | `right: {const: value}` |

Валидация на рантайме — `afb_bf_protocol.payload_validation.validate_alarm`
(тот же extra `[validation]`, что и `validate_tradeplan`/`validate_deal`).

## 12. Семантика операторов условий (condition.v1.json)

`spec/schemas/condition.v1.json` — единый источник истины словаря операторов
условия, на который ссылаются `deal.v2.json`, `tradeplan.v2.json` (частично —
без строгой матрицы пар, см. §10) и `alarm.v1.json`. Одна и та же семантика
применяется одинаково к алармам, торговым планам и сделкам. Эталонная
реализация (не только описание) — `afb_bf_protocol.condition_semantics`
(stdlib `decimal`, без побочных эффектов); BF и AFB обязаны вычислять условия
через эту библиотеку, а не переизобретать сравнения на месте.

**Источники (`left.source`) и допустимые операторы:**

Для `price` полностью поддерживаются шесть операторов — ни один не
устаревший: `touch`, `above`/`below`, `breakout`/`breakdown`/`crossing`. Они
различаются и типом исполняемой BF заявки: `touch` → **лимитная** (цена от
best bid/ask ± `limit_offset_steps`), остальные пять → **рыночная**
(исполняется безусловно, без ограничения проскальзывания) — решение
принимает исключительно `belphegor.plan_engine.order_policy`, на проводе
никакого поля типа заявки не передаётся (deprecated с v1.11.0 блок `order`
в `deal.v1.json`/`deal.v2.json`/`tradeplan.v2.json` больше не читается BF).

| `left.source` | `right` | Операторы | Семантика | Исполнение BF |
|---|---|---|---|---|
| `price` | `const` | **`touch`** (или `op` опущен — совместимость со старыми сделками/планами) | уровень пройден между prev и cur: `min(prev, cur) <= level <= max(prev, cur)` | лимитная |
| `price` | `const` (или `primitiveRef` в ТП) | **`above`**, **`below`** | inclusive level: `above` = `cur >= level`, `below` = `cur <= level`; опциональный `duration` (реальные непрерывные секунды на monotonic clock BF; только BF) | рыночная |
| `price` | `const` | **`breakout`**, **`breakdown`**, **`crossing`** + обязательный `timeframe` | по последней **закрытой** свече `timeframe`: `breakout` = `open < level AND close > level`; `breakdown` = `open > level AND close < level`; `crossing` = любое из двух. Никогда не вычисляется внутри бара. | рыночная |
| `indicator` | `const` или `indicator` | `above`, `below`, `crosses_above`, `crosses_below`, `crossing` | скалярное сравнение (см. ниже); `field` на проводе не передаётся | — (не создаёт заявку напрямую) |
| `dataset` (`positions`/`orders`/`hhi`/`trades`; `volume` — только в схеме) | `const` или `dataset` того же `dataset_id` | те же 5 скалярных | `field` **обязателен**; как индикаторы; `volume` временно не вычисляется | — |
| *deprecated*: `price` + `crosses_above`/`crosses_below`/тиковый `crossing` (без `timeframe`) | `const` | принимается | удаление в v2.0.0 | лимитная (как touch) |
| *deprecated*: `quote` (`bid`/`ask`) | `const` | принимается как раньше | из UI AFB убран; удаление в v2.0.0 | — |

**Скалярная семантика (5 операторов, `indicator`/`dataset` и deprecated
тиковые `price`/`quote`)** — с `cur`/`prev` слева и `ref_cur`/`ref_prev`
справа (для константы `ref_prev == ref_cur`):

- `above`: `cur > ref_cur` (на `price` с `op: above`/`below` — отдельная inclusive-семантика, см. `evaluate_price_level_op`)
- `below`: `cur < ref_cur`
- `crosses_above`: `prev <= ref_prev AND cur > ref_cur`
- `crosses_below`: `prev >= ref_prev AND cur < ref_cur`
- `crossing`: `crosses_above OR crosses_below`

Касание без ухода за уровень (`cur == ref_cur`) пересечением никогда не
считается. Граничная семантика **нестрогая** на стороне `prev`
(`<=`/`>=`, не `<`/`>`) — это специально фиксирует подтверждённый баг
пересечения (кейс 3.248 из логов аларма `alarm-5a01-4480-ba65`): при
`prev == ref` пересечение раньше не засчитывалось (использовалось строгое
`prev < ref`), хотя `cur` уже ушёл за уровень. И в AFB
(`_check_condition_two_series`), и в BF (`evaluate_event`) была одна и та же
дыра — фикс в общей библиотеке закрывает обе стороны разом.

**Защитное время (`duration`).** Опциональное целое ≥ 1 на price-условии с
`op: above|below` (после компиляции; UI может начать с `touch` и обязан
перевести оператор до публикации). BF держит условие истинным непрерывно
указанное число **реальных секунд** (monotonic clock): `false`, отсутствие
живых котировок для оценки, amend/pause/cancel условия и рестарт процесса BF
сбрасывают прогресс; прогресс **не** пишется в deal state. AFB-эмуляция
черновых планов и алармы поле игнорируют. Протокол **не** запрещает
`duration` одновременно на нескольких legs одной сделки — UI может
ограничивать «время или доли» отдельно.

Отсутствие данных (значение `None`/недоступно) в любой точке вычисления →
`False`, никогда исключение — инвариант BF сохраняется во всех трёх
компонентах.

## 13. Enrollment (пользовательская привязка ключей BF ↔ AFB)

Первичный обмен Ed25519-ключами и повторная привязка (ротация) идут не как
ручное копирование файлов, а как отдельный protocol-flow поверх того же
`ws://` (без TLS): одноразовый токен высокой энтропии + HMAC-подтверждение
публичных ключей обеими сторонами — активный MITM без токена не может
подменить ключ ни одной из сторон. Реализация — единая для обеих сторон
библиотека `afb_bf_protocol.enrollment` (не переизобретать на месте).

### 14.1 Пейринг-токен и строка привязки

**Токен**: `bf1_` + lowercase-base32-без-паддинга от `secrets.token_bytes(20)`
→ 36 символов, 160 бит энтропии. Никогда не логируется; наружу — только
внутри строки привязки. `PAIRING_TOKEN_PREFIX = "bf1_"`.

**Строка привязки** (то, что пользователь копирует из UI AFB и вставляет в
setup-мастер BF): `afbpair1_` + b64url-без-паддинга от
`canonical_json({"v": 1, "afb": "<afb_ws_url>", "bf": "<bf_id>", "tok": "bf1_…"})`.
`PAIRING_STRING_PREFIX = "afbpair1_"`. Секретность строки равна секретности
токена внутри неё; версия `v` даёт форвард-совместимость формата.

### 14.2 MAC-ключ и нонсы

```
K = HMAC-SHA256(key=UTF-8(token), msg=b"afb-bf-enroll.v1|kdf")
```

`ENROLL_CONTEXT = "afb-bf-enroll.v1"`. BF выводит `K` локально из токена,
полученного из строки привязки. AFB вычисляет `K` в момент выдачи токена и
хранит **только** `mac_key` (hex) + `token_sha256` + `expires_at` +
`attempts_left` — сам токен на AFB нигде не персистится.

`client_nonce`/`server_nonce` = `base64url(16 случайных байт)`.

### 14.3 Точные строки под HMAC-SHA256(K, ...)

```
MAC_request  = "afb-bf-enroll.v1|bf2afb|" + bf_id + "|" + client_nonce + "|" + sha256_hex(bf_public_key_pem)
MAC_response = "afb-bf-enroll.v1|afb2bf|" + bf_id + "|" + client_nonce + "|" + server_nonce + "|" + sha256_hex(afb_public_key_pem)
```

`bf_public_key_pem`/`afb_public_key_pem` — PEM-строка ровно как в JSON-поле
конверта (не перепарсенная); `sha256_hex` считается ДО парсинга ключа, чтобы
не парсить недоверенный ввод раньше MAC-проверки. `bf_id` ограничен
`^[A-Za-z0-9_-]{1,64}$`, нонсы — base64url, хэши — hex, так что разделитель
`|` не создаёт неоднозначности. Директиональные метки `bf2afb`/`afb2bf`
исключают отражение запроса как ответа; `bf_id` в MAC не даёт перенести
токен на другой коннектор; `client_nonce` в ответе даёт свежесть. Сравнение
MAC — только `hmac.compare_digest` (`afb_bf_protocol.enrollment.macs_equal`).

### 14.4 key_id как отпечаток ключа

`signature.key_id` конверта (и `public_key_id` в реестре AFB) — это
**отпечаток ключа**, не произвольная метка:

```
key_fingerprint(pub) = sha256(DER(SubjectPublicKeyInfo(pub))).hexdigest()[:12]
```

(`afb_bf_protocol.signing.key_fingerprint`). DER, а не PEM-строка — не зависит
от переносов строк. Обе стороны вычисляют его из самого ключа; поле не
валидируется как условие доверия (это делает MAC/подпись), а служит дешёвой
диагностической сверкой целостности при enrollment.

### 14.5 Обмен (один round-trip по тому же `/bf/v1`)

```mermaid
sequenceDiagram
    participant BF
    participant AFB

    BF->>BF: генерирует Ed25519-пару в памяти
    BF->>AFB: session.enroll_request (self-signed новым ключом)
    note right of BF: bf_id, client_nonce, bf_public_key (PEM),<br/>mac = MAC_request, protocol

    AFB->>AFB: shape-валидация → replay-дедуп →<br/>pending pairing (TTL/attempts) →<br/>timing-safe проверка MAC_request →<br/>парсинг ключа → сверка key_fingerprint
    AFB->>AFB: атомарно пишет PEM в secrets/bf_keys/{bf_id}.pem,<br/>мутирует реестр, рвёт живую сессию bf_id
    AFB->>BF: session.enroll_response (подписан боевым ключом AFB)
    note left of AFB: server_nonce, afb_public_key (PEM),<br/>mac = MAC_response, bf_name, protocol
    AFB->>BF: close 1000

    BF->>BF: проверяет MAC_response → парсит ключ AFB →<br/>проверяет им подпись конверта
    BF->>BF: только теперь атомарно персистит файлы<br/>(private key 0600)
    BF->>AFB: переподключение обычным session.hello (новым ключом)
```

1. **BF** генерирует Ed25519-пару в памяти, шлёт `session.enroll_request` —
   обычный конверт протокола, **self-signed** новым ключом (proof-of-possession;
   никакого `alg: "none"`), `signature.key_id` = отпечаток нового ключа.
2. **AFB**: shape-валидация → replay-дедуп (`message_id`) → находит запись
   реестра по `bf_id` → pending `pairing` (TTL, `attempts_left`) →
   timing-safe проверка `MAC_request` → парсинг присланного ключа →
   self-подпись собственным продовым ключом → сверка
   `key_fingerprint(bf_public_key) == envelope.signature.key_id`.
3. **AFB**: атомарно пишет PEM в `secrets/bf_keys/{bf_id}.pem` (tmp+`os.replace`),
   мутирует запись реестра (`public_key_file`, `public_key_id` = отпечаток,
   удаляет `pairing`), рвёт **живую** сессию этого `bf_id`, если была, отвечает
   `session.enroll_response` (подписан боевым ключом AFB): `server_nonce`,
   `afb_public_key` (PEM), `mac = MAC_response`, плюс `bf_name`/`protocol` —
   идентичность для конфига BF (эти два поля не под MAC; их целостность даёт
   Ed25519-подпись конверта уже доверенным ключом AFB). Закрывает сокет кодом
   **1000**.
4. **BF**: проверяет `MAC_response` timing-safe → парсит ключ AFB → проверяет
   им подпись конверта → **только теперь** атомарно персистит файлы (приватный
   ключ с правами 0600) → переподключается обычным подписанным
   `session.hello` новым ключом.
5. Любой отказ AFB на шаге 2 → close **4004 "enroll rejected"** без
   уточнения причины (нет оракула для подбора); при валидном pending pairing
   и неверном MAC — `attempts_left -= 1`, при достижении 0 — блок `pairing`
   удаляется целиком (нужен новый код от AFB).

Крах в середине не оставляет полусостояния: BF не пишет на диск до
верифицированного `MAC_response`. Гонка «AFB потребил токен, BF потерял
ответ» решается выдачей нового пейринг-кода — старый токен на AFB уже нельзя
использовать повторно (запись `pairing` заменяется/удаляется).

`enabled` коннектора **не** авто-включается по факту успешного enrollment —
это отдельное риск-решение менеджера; enrollment работает и при
`enabled: false`.

### 14.6 Перепривязка (ротация)

Тот же механизм используется для перевыпуска ключа BF, но инициируется
**только со стороны AFB**: `session.reenroll_request` (payload: `bf_id`,
опционально `reason`), подписанный боевым ключом AFB — команда «подними
setup-страницу для перепривязки». BF, получив её на живой сессии, поднимает
setup-мастер заново (торговля на старых ключах продолжается, пока новый
enrollment не завершится успехом). Старый ключ AFB заменяет только по факту
успешного `session.enroll_request` — до этого момента текущая сессия BF
остаётся рабочей.

### 14.7 Известный остаточный риск

Setup-страница свежей (ещё не привязанной) облачной BF на `ws://` открыта и
примет **любую** валидную строку привязки, в том числе не ту, что
предназначалась этому экземпляру — окно между разворачиванием BF и тем,
когда настоящий пользователь успевает вставить свой код. Приняли осознанно:
окно мало, есть rate-limit на попытки, а второй шаг (ввод брокерского токена)
чужой строкой у настоящего владельца аккаунта не пройдёт (брокер вернёт 403).
Рекомендация — привязывать сразу после запуска BF.

## 14. MQTT-уведомления информера (`afb.notification.alarm.v1`)

Схема: `spec/schemas/notification.alarm.v1.json`. Это **не**
wire-сообщение AFB↔BF и **не** подписанный конверт — AFB публикует JSON в MQTT
топик `<topic_base>/alarms/<user_id>` при срабатывании пользовательского
аларма; демон **informer** (`AFB/informer/`) подписывается и рассылает
Telegram/e-mail.

Поле `condition` повторяет `alarm.v1.json#/$defs/alarmConditionNode` (тот же
`conditionNode`, что в `afb.alarm.v1`). Блок `display` **обязателен** и
заполняется бэкендом AFB до публикации — человекочитаемые строки для
информера (зеркало карточек аларма во фронтенде). Информер **не** читает
`config/users` и securities — только MQTT.

| Поле | Смысл |
|---|---|
| `triggered_value` | значение, по которому сработало условие (цена, индикатор, поле dataset) |
| `instrument_price` | цена инструмента (`price_data.last`) в момент срабатывания |
| `timestamp` | добавляется `MQTTPublisher` при публикации (ISO-8601) |

Форматирование `display` — `afb_bf_protocol.alarm_display` (порт
`alarmConditionDescription.ts`). Валидация на рантайме —
`afb_bf_protocol.payload_validation.validate_notification` (extra
`[validation]`). Примеры: `examples/notifications/alarm.*.json`.

## 15. MQTT-уведомления о сделках (`afb.notification.deal.v1`)

Схема: `spec/schemas/notification.deal.v1.json`. Как и alarm-уведомления —
**не** wire-сообщение AFB↔BF, **не** подписанный конверт. AFB публикует JSON в
MQTT топик `<topic_base>/deals/<user_id>` при событиях жизненного цикла
сделки, на которые подписан пользователь (Настройки → Торговля); демон
**informer** рассылает Telegram/e-mail.

Поле `category` — одна из пяти категорий, которыми управляют пользовательские
тумблеры: `trigger` (триггер условия входа/выхода), `order_placed`
(выставление ордера), `order_executed` (исполнение ордера, полное или
частичное), `position` (изменение позиции на счёте), `close` (закрытие сделки
с финансовым результатом). Поле `event` хранит исходный wire-тип события
(`condition.triggered`, `order.filled` и т.п.) — только для трассируемости.

| Поле | Смысл |
|---|---|
| `at` | время события BF (`market_now_iso()`), прокинутое из payload исходного события `order.*`/`position.*`/`deal.*` — опционально, может отсутствовать у старых BF |
| `realized_pnl` | финансовый результат, заполняется для `category: close` |
| `timestamp` | добавляется `MQTTPublisher` при публикации (ISO-8601) |

Валидация — тот же `afb_bf_protocol.payload_validation.validate_notification`,
диспетчеризация по `obj["schema"]`. Примеры: `examples/notifications/deal.*.json`.
