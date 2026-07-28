from django.core.mail import EmailMultiAlternatives
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.conf import settings

def send_email_user(subject, template_name, context, to_email):
    """
    Sends an HTML email with an embedded logo image.

    - Renders an HTML template with context data
    - Sends an email using Django EmailMultiAlternatives
    - Attaches an inline image (logo) via Content-ID
    """

    html_content = render_to_string(template_name, context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )

    msg.attach_alternative(html_content, "text/html")

    path = finders.find('Logo.png') 

    if not path:
        raise FileNotFoundError("Logo not found in static files system")

    with open(path, "rb") as f:
        logo = MIMEImage(f.read())
        logo.add_header("Content-ID", "<logo>")
        logo.add_header("Content-Disposition", "inline", filename="Logo.png")
        msg.attach(logo)
    
    msg.send()