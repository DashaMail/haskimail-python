"""Send a batch of emails (up to 500) in one API call."""

from haskimail import ServerClient

client = ServerClient("ваш-серверный-токен")

responses = client.send_email_batch([
    {
        "From": "noreply@example.com",
        "To": "user1@example.com",
        "Subject": "Уведомление для User 1",
        "TextBody": "Привет, User 1!",
        "MessageStream": "outbound",
    },
    {
        "From": "noreply@example.com",
        "To": "user2@example.com",
        "Subject": "Уведомление для User 2",
        "TextBody": "Привет, User 2!",
        "MessageStream": "outbound",
    },
])

for resp in responses:
    if resp.get("ErrorCode", 0) == 0:
        print(f"OK: {resp['To']} → {resp['MessageID']}")
    else:
        print(f"Ошибка: {resp['To']} → {resp['Message']}")
