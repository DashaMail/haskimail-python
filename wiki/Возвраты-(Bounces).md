# Возвраты (Bounces)

## Статистика доставки

```python
from haskimail import ServerClient

client = ServerClient("ваш-серверный-токен")

stats = client.get_delivery_statistics()

print(f"Неактивных адресов: {stats['InactiveMails']}")
for bt in stats.get("Bounces", []):
    print(f"  {bt['Name']}: {bt['Count']}")
```

## Список возвратов

```python
bounces = client.get_bounces(
    count=50,
    offset=0,
    type="HardBounce",
    fromdate="2026-01-01",
    todate="2026-06-01",
)

print(f"Всего: {bounces['TotalCount']}")
for b in bounces["Bounces"]:
    print(f"  {b['Email']} — {b['Type']} — {b['Description']}")
```

### Параметры фильтрации

| Параметр | Тип | Описание |
|----------|-----|----------|
| `count` | int | Макс. количество (до 500) |
| `offset` | int | Смещение для пагинации |
| `type` | string | Тип: `HardBounce`, `SoftBounce`, `SpamComplaint`, `Transient` |
| `fromdate` | string | Дата начала (ISO 8601) |
| `todate` | string | Дата конца |
| `emailFilter` | string | Фильтр по email |
| `tag` | string | Фильтр по тегу |
| `messageID` | string | Фильтр по ID сообщения |
| `messagestream` | string | ID канала |
