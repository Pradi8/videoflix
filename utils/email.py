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

    # Render HTML content from template
    html_content = render_to_string(template_name, context)

    # Create email message object
    msg = EmailMultiAlternatives(
        subject=subject,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )

    # Attach HTML version of the email
    msg.attach_alternative(html_content, "text/html")

    # Find logo file in Django static files
    path = finders.find('Logo.png') 

    # Ensure logo exists
    if not path:
        raise FileNotFoundError("Logo not found in static files system")

    # Attach logo as inline image
    with open(path, "rb") as f:
        logo = MIMEImage(f.read())
        # Content-ID allows referencing image inside HTML (cid:logo)
        logo.add_header("Content-ID", "<logo>")
        # Mark image as inline attachment
        logo.add_header("Content-Disposition", "inline", filename="Logo.png")
        msg.attach(logo)
    
    # Send email
    msg.send()