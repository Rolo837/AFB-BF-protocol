# Examples (fixtures)

Подписанные примеры конвертов — по одному на тип сообщения. Используются тестами
(`python/tests/`) и как справочник по формату.

- `examples/<type>.json` — готовый подписанный конверт (как на проводе).
- `examples/_payloads/<type>.json` — исходное тело payload (источник для генерации).
- `examples/_keys/` — **тестовые** ключи Ed25519 (детерминированы из фиксированного
  seed). Только для fixtures/тестов; **никогда** не использовать на реальном
  соединении.

## Происхождение payload'ов

Тела payload взяты из **реальных данных BF** (журналы `state/trading_events/*.jsonl`
и `state/deals/*.yaml`) для событий BF→AFB, и из канона протокола для команд
AFB→BF. Конверты пере-подписаны тестовым ключом под текущей таксономией
(транспортные сообщения раньше назывались `bf.*` / `execution_deal.*`).

Регенерация:

```bash
python -m afb_bf_protocol.tools.make_fixtures
```

## Покрытие

Покрыты 20 типов: полный handshake, жизненный цикл сделки и торговые события
(достаточно для end-to-end проверки). Остальные типы из `MESSAGE_REGISTRY`
(`broker.*`, `daemon.restart`, `deal.resync`, `deal.signal`, `order.partially_filled`,
`order.cancelled`, `order.rejected`, `position.changed`, `position.closed`,
`daemon.error`) добавляются по мере необходимости: положите тело в
`_payloads/<type>.json` и перезапустите генератор.
