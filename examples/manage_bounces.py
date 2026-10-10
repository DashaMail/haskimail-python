"""Work with bounces: delivery statistics and the list of bounces."""

from haskimail import ServerClient

client = ServerClient("ваш-серверный-токен")

# Общая статистика доставки
stats = client.get_delivery_statistics()
print(f"Неактивных адресов: {stats['InactiveMails']}")
for bounce_type in stats.get("Bounces", []):
    print(f"  {bounce_type['Name']}: {bounce_type['Count']}")

# Получить последние жёсткие возвраты
bounces = client.get_bounces(count=10, type="HardBounce")
for bounce in bounces["Bounces"]:
    print(f"{bounce['Email']} — {bounce['Description']} ({bounce['BouncedAt']})")
