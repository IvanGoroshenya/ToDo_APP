import os
import requests

# Данные Mailgun
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "c274fefbdba052334d2551744637bfba-7113c52e-f13a12d2")  # Ваш API-ключ
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "sandboxcb53aa640bcc4480af5019c37467df86.mailgun.org")  # Ваш домен
MAILGUN_BASE_URL = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

# Функция отправки письма
def send_email(subject, text, recipient_email):
    response = requests.post(
        MAILGUN_BASE_URL,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": "Test Mailgun <mailgun@sandboxcb53aa640bcc4480af5019c37467df86.mailgun.org>",
            "to": recipient_email,
            "subject": subject,
            "text": text
        }
    )

    if response.status_code == 200:
        print("Email отправлен успешно!")
    else:
        print(f"Ошибка при отправке email ({response.status_code}): {response.text}")

# Пример отправки письма
send_email(
    subject="Тестовое уведомление",
    text="Привет! Это тестовое уведомление через Mailgun.",
    recipient_email="xgzgsy@gmail.com"  # Ваш верифицированный email
)
