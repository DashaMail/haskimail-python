# Стоп-листы (Suppressions)

Стоп-листы содержат email-адреса, на которые не будут отправляться письма. Привязаны к конкретному каналу сообщений.

## Получить стоп-лист

```python
from haskimail import ServerClient

client = ServerClient("ваш-серверный-токен")

suppressions = client.get_suppressions(
    "outbound",
    SuppressionReason="HardBounce",
    Origin="Recipient",
    fromdate="2026-01-01",
)

for s in suppressions["Suppressions"]:
    print(f"{s['EmailAddress']} — {s['SuppressionReason']} ({s['CreatedAt']})")
```

### Параметры фильтрации

| Параметр | Тип | Описание |
|----------|-----|----------|
| `SuppressionReason` | string | `"HardBounce"`, `"SpamComplaint"`, `"ManualSuppression"` |
| `Origin` | string | `"Recipient"`, `"Customer"`, `"Admin"` |
| `fromdate` | string | Дата начала |
| `todate` | string | Дата конца |
| `EmailAddress` | string | Фильтр по email |

## Добавить в стоп-лист

```python
result = client.create_suppressions("outbound", {
    "Suppressions": [
        {"EmailAddress": "spam@example.com"},
        {"EmailAddress": "unsubscribed@example.com"},
    ]
})

for s in result["Suppressions"]:
    print(f"{s['EmailAddress']}: {s['Status']}")
```

## Удалить из стоп-листа

```python
result = client.delete_suppressions("outbound", {
    "Suppressions": [
        {"EmailAddress": "reactivated@example.com"},
    ]
})

for s in result["Suppressions"]:
    print(f"{s['EmailAddress']}: {s['Status']}")
```
