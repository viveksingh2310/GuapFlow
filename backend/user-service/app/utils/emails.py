from fastapi_mail import ConnectionConfig

# Ideally, load these from environment variables (.env)
email_conf = ConnectionConfig(
    MAIL_USERNAME="viveksingh102303@gmail.com",
    MAIL_PASSWORD="yzyerfnkmyngrjik",
    MAIL_FROM="viveksingh102303@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)