from django.test import TestCase
from main.services.phone_validation_service import validate_landline
from main.services.phone_validation_service import validate_mobile
from django.core.exceptions import ValidationError


class TestPhoneValidationService(TestCase):

    # Mobile Tests
    def test_validate_mobile_when_valid_without_plus(self):
        self.assertEqual(validate_mobile('0418502729'), '+61418502729')

    def test_validate_mobile_when_valid_without_plus_and_spaces(self):
        self.assertEqual(validate_mobile('0418 502 729'), '+61418502729')

    def test_validate_mobile_when_valid_with_plus(self):
        self.assertEqual(validate_mobile('+61418502729'), '+61418502729')

    def test_validate_mobile_when_valid_with_plus_and_spaces(self):
        self.assertEqual(validate_mobile('+61 418 502 729'), '+61418502729')

    def test_validate_mobile_when_invalid_with_plus(self):
        with self.assertRaises(ValidationError):
            validate_mobile('+61 418 502 72')

    def test_validate_mobile_when_invalid_without_plus(self):
        with self.assertRaises(ValidationError):
            validate_mobile('6141850272')

    # Landline Tests
    def test_validate_landline_when_valid_without_plus(self):
        self.assertEqual(validate_landline('0894571664'), '+61894571664')

    def test_validate_landline_when_valid_without_plus_and_spaces(self):
        self.assertEqual(validate_landline('02 9457 1664'), '+61294571664')

    def test_validate_landline_when_valid_with_plus(self):
        self.assertEqual(validate_landline('+61318502729'), '+61318502729')

    def test_validate_landline_when_valid_with_plus_and_spaces(self):
        self.assertEqual(validate_landline('+61 7 9457 0000'), '+61794570000')

    def test_validate_landline_when_invalid_with_plus(self):
        with self.assertRaises(ValidationError):
            validate_landline('+61 418 502 72')

    def test_validate_landline_when_invalid_without_plus(self):
        with self.assertRaises(ValidationError):
            validate_landline('6141850272')
