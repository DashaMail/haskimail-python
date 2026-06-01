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

## Детали возврата

```python
bounce = client.get_bounce(12345)

print(f"Email: {bounce['Email']}")
print(f"Тип: {bounce['Type']}")
print(f"Описание: {bounce['Description']}")
print(f"Дата: {bounce['BouncedAt']}")
```

## SMTP-дамп возврата

```python
dump = client.get_bounce_dump(12345)
print(dump["Body"])  # Полный SMTP-ответ сервера
```

## Реактивация получателя

```python
result = client.activate_bounce(12345)
print(f"Реактивирован: {result['Email']}")
```

> **Важно:** Реактивировать можно только получателей с жёстким возвратом (HardBounce). Жалобы на спам (SpamComplaint) реактивировать нельзя.
