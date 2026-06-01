"""Demonstrate the typed exception hierarchy."""

from haskimail import (
    ApiInputError,
    HttpError,
    InactiveRecipientsError,
    InvalidAPIKeyError,
    RateLimitExceededError,
    ServerClient,
)

client = ServerClient("ваш-серверный-токен")

try:
    client.send_email({
        "From": "sender@example.com",
        "To": "recipient@example.com",
        "Subject": "Тест",
        "TextBody": "Привет!",
    })
    print("Письмо отправлено!")

except InactiveRecipientsError as e:
    # Получатель ранее вернул hard bounce или пожаловался на спам
    print(f"Неактивные получатели: {', '.join(e.recipients)}")
    print("Вы можете реактивировать их через client.activate_bounce()")

except InvalidAPIKeyError:
    print("Неверный API-токен! Проверьте настройки сервера.")

except RateLimitExceededError:
    import time
    print("Слишком много запросов. Ждём 10 секунд...")
    time.sleep(10)

except ApiInputError as e:
    # Любая ошибка 422 (неверные данные)
    print(f"Ошибка API: {e.message}")
    print(f"Код ошибки: {e.error_code}")

except HttpError as e:
    # Любая другая HTTP-ошибка (500, 503, и т.д.)
    print(f"HTTP {e.status_code}: {e.message}")
