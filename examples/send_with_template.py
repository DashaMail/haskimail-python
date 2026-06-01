"""Send an email using a pre-defined template."""

from haskimail import ServerClient

client = ServerClient("ваш-серверный-токен")

response = client.send_email_with_template({
    "TemplateAlias": "welcome",
    "From": "support@example.com",
    "To": "newuser@example.com",
    "TemplateModel": {
        "product_name": "Мой Сервис",
        "user_name": "Иван",
        "action_url": "https://example.com/activate",
    },
    "MessageStream": "outbound",
})

print(f"Отправлено по шаблону! MessageID: {response['MessageID']}")
