from django.core.mail import EmailMultiAlternatives
from main.models import EmailConfiguration


def send_email(email_type, to_email, subject, html_content, plain_content):
    email = prepare_email(email_type, to_email, subject, html_content, plain_content)
    email.send()


def prepare_email(email_type, to_email, subject, html_content, plain_content):
    email_configuration = EmailConfiguration.objects.get(type=email_type.value)

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_content,
        from_email=email_configuration.from_email,
        to=[to_email]
    )

    if email_configuration.bcc_email:
        email.bcc=[email_configuration.bcc_email]

    if email_configuration.cc_email:
        email.cc=[email_configuration.cc_email]

    email.attach_alternative(html_content, "text/html")

    return email
