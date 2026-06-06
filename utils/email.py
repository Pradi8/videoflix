from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
import os
from django.conf import settings

def send_email_user(subject, template_name, context, to_email):
    html_content = render_to_string(template_name, context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )

    msg.attach_alternative(html_content, "text/html")

    logo_path = os.path.join(settings.BASE_DIR, "emails/static/images/Logo.svg")   

    with open(logo_path, "rb") as f:
        logo = MIMEImage(f.read())
        logo.add_header("Content-ID", "<logo>")
        logo.add_header("Content-Disposition", "inline")
        msg.attach(logo)

    msg.send()