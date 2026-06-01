"""CRUD operations on email templates."""

from haskimail import ServerClient

client = ServerClient("ваш-серверный-токен")

# Создать шаблон
template = client.create_template({
    "Name": "Приветственное письмо",
    "Alias": "welcome",
    "Subject": "Добро пожаловать, {{name}}!",
    "HtmlBody": "<h1>Привет, {{name}}!</h1><p>Рады видеть вас в {{product}}.</p>",
    "TextBody": "Привет, {{name}}! Рады видеть вас в {{product}}.",
})
print(f"Создан шаблон ID: {template['TemplateId']}")

# Список шаблонов
templates = client.get_templates(count=100)
for t in templates["Templates"]:
    print(f"  [{t['TemplateId']}] {t['Name']} (alias: {t.get('Alias', '—')})")

# Валидировать шаблон
validation = client.validate_template({
    "Subject": "{{subject}}",
    "HtmlBody": "{{content}}",
    "TestRenderModel": {"subject": "Тест", "content": "Привет!"},
})
print(f"Валидация: AllContentIsValid={validation.get('AllContentIsValid')}")

# Удалить шаблон
client.delete_template(template["TemplateId"])
print("Шаблон удалён.")
