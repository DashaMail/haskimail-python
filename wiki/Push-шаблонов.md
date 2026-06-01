# Push шаблонов

Перенос шаблонов между серверами доступен через `AccountClient`.

```python
from haskimail import AccountClient

account = AccountClient("ваш-аккаунт-токен")
```

## Push шаблонов

```python
result = account.push_templates({
    "SourceServerID": 1,
    "DestinationServerID": 2,
    "PerformChanges": True,
})

print(f"Всего шаблонов: {result['TotalCount']}")
for t in result.get("Templates", []):
    print(f"  {t['Alias']}: {t['Action']}")
```

### Параметры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `SourceServerID` | int | ID сервера-источника |
| `DestinationServerID` | int | ID сервера-назначения |
| `PerformChanges` | bool | `True` — применить изменения; `False` — только просмотр (dry run) |

### Dry Run

Для предварительного просмотра изменений:

```python
preview = account.push_templates({
    "SourceServerID": 1,
    "DestinationServerID": 2,
    "PerformChanges": False,
})

for t in preview.get("Templates", []):
    print(f"  {t['Alias']}: {t['Action']}")  # Create, Update, None
```
