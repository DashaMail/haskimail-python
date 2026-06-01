"""Manage domains with the Account API."""

from haskimail import AccountClient

account = AccountClient("ваш-аккаунт-токен")

# Список доменов
domains = account.get_domains()
for d in domains["Domains"]:
    print(
        f"{d['Name']} — "
        f"DKIM: {'✓' if d['DKIMVerified'] else '✗'}, "
        f"SPF: {'✓' if d['SPFVerified'] else '✗'}, "
        f"ReturnPath: {'✓' if d['ReturnPathDomainVerified'] else '✗'}"
    )

# Добавить домен
domain = account.create_domain({"Name": "newdomain.ru"})
print(f"\nДомен создан (ID: {domain['ID']})")
print(f"DKIM-запись: {domain['DKIMHost']} → {domain['DKIMTextValue']}")
print(f"SPF-запись: {domain['SPFHost']} → {domain['SPFTextValue']}")

# Проверить DNS после настройки
dkim = account.verify_domain_dkim(domain["ID"])
print(f"DKIM проверен: {dkim['DKIMVerified']}")

spf = account.verify_domain_spf(domain["ID"])
print(f"SPF проверен: {spf['SPFVerified']}")
