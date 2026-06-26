# AFB-BF-protocol

Единый источник истины бизнес-протокола между **AFB** (OMS: анализ графиков и
торговые планы) и **BF** (демон-исполнитель сделок через API брокеров).

Версия провода: **`afb.execution.v1`**. Транспорт v1 — WebSocket; формат конверта
не привязан к транспорту (задел под MQTT и др.). Каждое сообщение — подписанный
(Ed25519) JSON-конверт.

## Что внутри

```
spec/
  asyncapi.yaml          # КАНОН: AsyncAPI 3.1, все типы сообщений
  schemas/
    envelope.json        # схема конверта (контракт подписи/хэша)
    deal.v1.json         # сделка afb.deal.v1
    deal.v2.json         # сделка afb.deal.v2 (мульти-вход/выход)
    deal_state.v2.json   # общая on-disk схема состояния сделки
    payloads/*.json      # схема payload каждого типа сообщения
examples/                # подписанные примеры конвертов (fixtures) + тестовые ключи
docs/MESSAGES.md         # СГЕНЕРИРОВАНО из спеки — каталог сообщений
python/                  # пакет afb-bf-protocol (модели, подпись, валидация, таксономия)
VERSIONING.md            # политика версий провода и пакета
```

## Подключение в AFB и BF

Пакет ставится по git-тегу (без публикации в PyPI):

```
# requirements.txt / pyproject.toml
afb-bf-protocol @ git+https://github.com/Rolo837/AFB-BF-protocol.git@v1.0.0#subdirectory=python
```

Использование:

```python
from afb_bf_protocol import (
    make_envelope, sign_envelope, verify_envelope,
    load_private_key, load_public_key,
    Envelope, MESSAGE_REGISTRY, validate_envelope_fields, ReplayCache,
)

env = make_envelope(
    sender="afb", recipient="finam-arena-316", msg_type="deal.operation",
    payload={"operations": [{"deal_id": "d1", "revision": 1, "op": "activate"}]},
    key_id="afb-local-1",
)
sign_envelope(env, load_private_key("secrets/afb-private.pem"))
wire = env.to_dict()                       # -> send over WebSocket
```

Публичный API ядра:

- **Конверт/подпись:** `Envelope`, `Signature`, `make_envelope`, `sign_envelope`,
  `verify_envelope`, `canonical_json`, `payload_hash`, `signing_string`.
- **Ключи:** `load_private_key`/`load_public_key` (PEM или raw-32), `generate_keypair`,
  `export_*_pem`, `ensure_dev_keypair`.
- **Валидация транспорта:** `validate_envelope_fields`, `validate_envelope_shape`,
  `ReplayCache`, `ProtocolValidationError`.
- **Таксономия:** `MESSAGE_REGISTRY`, `COMMAND_TYPES`, `BF_EVENT_TYPES`,
  `PERSISTED_BF_EVENT_TYPES`, `SUPPORTED_MARKETS`.
- **Состояние:** `DealState`, `DealStatus`, `safe_deal_filename`, `archived_deal_filename`.

> Глубокая бизнес-валидация сделки (дерево условий, режимы сайзинга, percent v2)
> остаётся в BF — она не дублируется в AFB и зависит от доменных модулей BF.
> Структурную валидацию payload обеспечивают JSON-схемы в `spec/`.

## Разработка

```bash
cd python && pip install -e ".[dev]"
pytest                                   # схемы, подпись, эквивалентность с BF/AFB
afb-bf-protocol-generate                 # перегенерировать taxonomy.py и docs/ из спеки
python -m afb_bf_protocol.tools.make_fixtures   # пересобрать examples/
npx @asyncapi/cli validate spec/asyncapi.yaml
```

Канон — `spec/`. `taxonomy.py` и `docs/MESSAGES.md` **генерируются** из спеки
(`afb-bf-protocol-generate`); не редактировать вручную. Политика версий —
[`VERSIONING.md`](VERSIONING.md).
