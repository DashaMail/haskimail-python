# Haskimail Python

<img src="https://haskimail.ru/assets/images/haskimail_logo.svg" alt="Haskimail" width="200">

Официальная Python-библиотека для [Haskimail HTTP API](https://haskimail.ru/developer).

## Установка

```bash
pip install haskimail
```

## Использование

### Отправка письма

```python
from haskimail import ServerClient

client = ServerClient("ваш-серверный-токен")

response = client.send_email({
    "From": "отправитель@домен.ru",
    "To": "получатель@домен.ru",
    "Subject": "Привет от Haskimail!",
    "HtmlBody": "<h1>Привет!</h1><p>Это письмо отправлено через Haskimail.</p>",
    "TextBody": "Привет! Это письмо отправлено через Haskimail.",
    "MessageStream": "outbound",
})

print(f"ID сообщения: {response['MessageID']}")
```

### Отправка с шаблоном

```python
response = client.send_email_with_template({
    "TemplateId": 42,
    "From": "отправитель@домен.ru",
    "To": "получатель@домен.ru",
    "TemplateModel": {
        "product_name": "Мой Сервис",
        "user_name": "Иван",
    },
})
```

### Пакетная отправка

```python
# До 500 писем за один запрос
responses = client.send_email_batch([
    {
        "From": "отправитель@домен.ru",
        "To": "user1@example.com",
        "Subject": "Привет, User 1!",
        "TextBody": "Сообщение для User 1",
    },
    {
        "From": "отправитель@домен.ru",
        "To": "user2@example.com",
        "Subject": "Привет, User 2!",
        "TextBody": "Сообщение для User 2",
    },
])
```

### Управление возвратами (bounces)

```python
# Получить статистику доставки
stats = client.get_delivery_statistics()

# Список возвратов
bounces = client.get_bounces(count=50, type="HardBounce")

# Реактивировать получателя
client.activate_bounce(bounce_id=12345)
```

### Шаблоны

```python
# Список шаблонов
templates = client.get_templates(count=100)

# Создать шаблон
template = client.create_template({
    "Name": "Приветственное письмо",
    "Subject": "Добро пожаловать, {{name}}!",
    "HtmlBody": "<h1>Привет, {{name}}!</h1>",
    "TextBody": "Привет, {{name}}!",
})

# Редактировать шаблон
client.edit_template(template["TemplateId"], {
    "Subject": "Обновлённая тема",
})

# Валидировать шаблон
result = client.validate_template({
    "Subject": "{{subject}}",
    "HtmlBody": "{{content}}",
    "TestRenderModel": {"subject": "Тест", "content": "Привет!"},
})
```

### Каналы сообщений (Message Streams)

```python
# Список каналов
streams = client.get_message_streams()

# Создать канал
stream = client.create_message_stream({
    "ID": "notifications",
    "Name": "Уведомления",
    "MessageStreamType": "Transactional",
})

# Архивировать канал
client.archive_message_stream("notifications")
```

### Стоп-листы (Suppressions)

```python
# Получить стоп-лист для канала
suppressions = client.get_suppressions("outbound", SuppressionReason="HardBounce")

# Добавить в стоп-лист
client.create_suppressions("outbound", {
    "Suppressions": [{"EmailAddress": "bad@example.com"}]
})

# Удалить из стоп-листа
client.delete_suppressions("outbound", {
    "Suppressions": [{"EmailAddress": "bad@example.com"}]
})
```

### Вебхуки

```python
# Создать вебхук
webhook = client.create_webhook({
    "Url": "https://example.com/webhooks/haskimail",
    "MessageStream": "outbound",
    "Triggers": {
        "Open": {"Enabled": True},
        "Click": {"Enabled": True},
        "Delivery": {"Enabled": True},
        "Bounce": {"Enabled": True, "IncludeContent": True},
    },
})

# Список вебхуков
webhooks = client.get_webhooks()
```

### Статистика

```python
# Общий обзор
overview = client.get_outbound_overview(
    fromdate="2026-01-01",
    todate="2026-06-01",
    messagestream="outbound",
)

# Отправки по дням
sent = client.get_sent_counts(tag="welcome")

# Открытия по платформам
platforms = client.get_email_open_platform_usage()

# Клики по браузерам
browsers = client.get_click_browser_usage()
```

## AccountClient

Для операций на уровне аккаунта (управление серверами, доменами, подписями отправителей) используйте `AccountClient`:

```python
from haskimail import AccountClient

account = AccountClient("ваш-аккаунт-токен")
```

### Домены

```python
# Список доменов
domains = account.get_domains()

# Добавить домен
domain = account.create_domain({"Name": "example.com"})

# Проверить DKIM
account.verify_domain_dkim(domain["ID"])

# Проверить SPF
account.verify_domain_spf(domain["ID"])

# Ротация DKIM-ключа
account.rotate_domain_dkim(domain["ID"])
```

### Серверы

```python
# Список серверов
servers = account.get_servers()

# Создать сервер
server = account.create_server({
    "Name": "Production",
    "Color": "Green",
})

# Редактировать сервер
account.edit_server(server["ID"], {"Name": "Production v2"})
```

### Подписи отправителей

```python
# Создать подпись
signature = account.create_sender_signature({
    "Name": "Отдел продаж",
    "FromEmail": "sales@example.com",
})

# Подтвердить SPF
account.verify_sender_signature_spf(signature["ID"])

# Запросить новый DKIM
account.request_new_dkim_for_sender_signature(signature["ID"])
```

### Push шаблонов

```python
# Перенести шаблоны между серверами
account.push_templates({
    "SourceServerID": 1,
    "DestinationServerID": 2,
    "PerformChanges": True,
})
```

### Удаление данных (GDPR)

```python
result = account.request_data_removal({
    "RequestedBy": "admin@example.com",
    "RequestedFor": "user@example.com",
})

status = account.get_data_removal_status(result["ID"])
```

## Обработка ошибок

Библиотека использует типизированную иерархию исключений:

```python
from haskimail import (
    ServerClient,
    HaskimailError,         # Базовое исключение
    HttpError,              # Ошибка HTTP-уровня
    InvalidAPIKeyError,     # 401 — неверный или отсутствующий токен
    ApiInputError,          # 422 — ошибка в данных запроса
    InactiveRecipientsError,  # 422/406 — неактивный получатель
    InvalidEmailRequestError, # 422/300 — неверный формат email
    RateLimitExceededError, # 429 — превышен лимит запросов
    InternalServerError,    # 500 — ошибка сервера
    ServiceUnavailableError,  # 503 — сервис недоступен
    UnknownError,           # Другие HTTP-ошибки
)

client = ServerClient("ваш-токен")

try:
    client.send_email({
        "From": "sender@example.com",
        "To": "recipient@example.com",
        "Subject": "Test",
        "TextBody": "Hello",
    })
except InactiveRecipientsError as e:
    print(f"Неактивные получатели: {e.recipients}")
except InvalidAPIKeyError:
    print("Проверьте API-токен!")
except RateLimitExceededError:
    print("Слишком много запросов, подождите...")
except ApiInputError as e:
    print(f"Ошибка в данных: {e.message} (код: {e.error_code})")
except HttpError as e:
    print(f"HTTP-ошибка {e.status_code}: {e.message}")
```

## Context Manager

Клиент можно использовать как контекстный менеджер для автоматического закрытия HTTP-сессии:

```python
with ServerClient("ваш-токен") as client:
    client.send_email({...})
# Сессия автоматически закрыта
```

## Тестирование

Для тестов используйте токен `HASKIMAIL_API_TEST` — письма будут валидированы, но не отправлены:

```python
client = ServerClient("HASKIMAIL_API_TEST")
response = client.send_email({...})  # Не доставится, но проверит данные
```

## Настройка

```python
client = ServerClient(
    "ваш-токен",
    base_url="https://api.haskimail.ru",  # по умолчанию
    timeout=30,                            # таймаут в секундах
)
```

## Требования

- Python 3.10+
- requests >= 2.28.0

## Ссылки

- [Документация API Haskimail](https://haskimail.ru/developer)
- [haskimail.js](https://github.com/Dashamail/haskimail.js) — Node.js SDK
- [haskimail.java](https://github.com/Dashamail/haskimail.java) — Java SDK
- [haskimail-php](https://github.com/Dashamail/haskimail-php) — PHP SDK

## Лицензия

MIT
