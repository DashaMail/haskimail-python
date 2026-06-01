"""Send an email with file attachments."""

import base64
from pathlib import Path

from haskimail import ServerClient

client = ServerClient("ваш-серверный-токен")

file_path = Path("report.pdf")
file_content = base64.b64encode(file_path.read_bytes()).decode()

response = client.send_email({
    "From": "reports@example.com",
    "To": "manager@example.com",
    "Subject": "Ежемесячный отчёт",
    "TextBody": "Отчёт за май 2026 во вложении.",
    "Attachments": [
        {
            "Name": "report-may-2026.pdf",
            "Content": file_content,
            "ContentType": "application/pdf",
        }
    ],
    "MessageStream": "outbound",
})

print(f"Письмо с вложением отправлено! MessageID: {response['MessageID']}")
