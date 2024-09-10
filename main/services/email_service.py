from django.core.mail import EmailMultiAlternatives


def send_email(to_email, subject, html_content, plain_content):

    from_email = 'mrmansly@iinet.net.au'

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_content,
        from_email=from_email,
        to=[to_email]
    )
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
    except Exception as e:
        print(f"Error send email: {e}")


