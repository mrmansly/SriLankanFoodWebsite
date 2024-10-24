from django.test import TestCase
from main.models import EmailConfiguration
from main.enums import EmailConfigurationType
from main.services.email_service import prepare_email


class TestEmailService(TestCase):

    def test_prepare_email(self):
        self.emailConfig1 = EmailConfiguration.objects.create(
            type=EmailConfigurationType.ORDER_CONFIRMATION.value,
            from_email='test@discard.com',
            cc_email='cctest@discard.com',
            bcc_email='bcctest@discard.com'
        )

        email = prepare_email(EmailConfigurationType.ORDER_CONFIRMATION,
                              "toemail@discard.com",
                              "subject",
                              "html_email",
                              "text_email")

        self.validate_common_data(email)
        self.assertEqual(email.cc, [self.emailConfig1.cc_email])
        self.assertEqual(email.bcc, [self.emailConfig1.bcc_email])

    def test_prepare_email_without_cc_or_bcc(self):
        self.emailConfig1 = EmailConfiguration.objects.create(
            type=EmailConfigurationType.ORDER_CONFIRMATION.value,
            from_email='test@discard.com'
        )

        email = prepare_email(EmailConfigurationType.ORDER_CONFIRMATION,
                              "toemail@discard.com",
                              "subject",
                              "html_email",
                              "text_email")

        self.validate_common_data(email)
        self.assertEqual(len(email.cc), 0)
        self.assertEqual(len(email.bcc), 0)

    def validate_common_data(self, email):
        self.assertEqual(email.subject, "subject")
        self.assertEqual(email.to, ["toemail@discard.com"])
        self.assertEqual(email.from_email, self.emailConfig1.from_email)
        self.assertEqual(email.body, "text_email")
        self.assertEqual(len(email.alternatives), 1)
        self.assertEqual(email.alternatives[0],('html_email', 'text/html'))
