"""Send a single email with Haskimail."""

from haskimail import ServerClient

client = ServerClient("ваш-серверный-токен")

response = client.send_email({
    "From": "отправитель@домен.ru",
    "To": "получатель@домен.ru",
    "Subject": "Привет от Haskimail!",
    "HtmlBody": "<h1>Привет!</h1><p>Это тестовое письмо.</p>",
    "TextBody": "Привет! Это тестовое письмо.",
    "Tag": "welcome",
    "TrackOpens": True,
    "TrackLinks": "HtmlAndText",
    "MessageStream": "outbound",
})

print(f"Отправлено! MessageID: {response['MessageID']}")
