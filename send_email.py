from utils.email import send_email_user

send_email_user(
    subject="Confirm your email",
    template_name="emails/confirm.html",
    context={"user.name": 42},
    to_email="user@example.com",
)