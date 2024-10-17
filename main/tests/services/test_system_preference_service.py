from django.test import TestCase
from main.models import SystemPreference
from main.services.system_preference_service import is_enabled, get_value, get_preference


class TestSystemPreferenceService(TestCase):

    def setUp(self):
        self.booleanTruePreference = SystemPreference.objects.create(
            name='booleanTruePreference',
            value='True',
            type='boolean'
        )

        self.booleanFalsePreference = SystemPreference.objects.create(
            name='booleanFalsePreference',
            value='False',
            type='boolean'
        )

        self.booleanInvalidPreference = SystemPreference.objects.create(
            name='invalidBooleanPreference',
            value='Value',
            type='boolean'
        )

        self.stringPreference = SystemPreference.objects.create(
            name='stringPreference',
            value='Value',
            type='string'
        )

        self.intPreference = SystemPreference.objects.create(
            name='intPreference',
            value='10',
            type='int'
        )

        self.invalidIntPreference = SystemPreference.objects.create(
            name='invalidIntPreference',
            value='a',
            type='int'
        )

        self.floatPreference = SystemPreference.objects.create(
            name='floatPreference',
            value='10.15',
            type='float'
        )

        self.invalidFloatPreference = SystemPreference.objects.create(
            name='invalidFloatPreference',
            value='a',
            type='float'
        )

        self.invalidTypePreference = SystemPreference.objects.create(
            name='invalidTypePreference',
            value='10.15',
            type='invalid'
        )

    def test_get_preference_when_exists(self):
        self.assertTrue(get_preference(self.stringPreference.name) is not None)

    def test_get_preference_when_not_exists(self):
        with self.assertRaises(ValueError):
            get_preference('nonExistingPreference')

    def test_is_enabled_with_true(self):
        self.assertTrue(is_enabled(self.booleanTruePreference.name))

    def test_is_enabled_with_false(self):
        self.assertFalse(is_enabled(self.booleanFalsePreference.name))

    def test_is_enabled_with_invalid_value(self):
        with self.assertRaises(ValueError):
            is_enabled(self.booleanInvalidPreference.name)

    def test_is_enabled_with_string_type(self):
        with self.assertRaises(ValueError):
            is_enabled(self.stringPreference.name)

    def test_get_value_with_string(self):
        self.assertEqual(get_value(self.stringPreference.name), self.stringPreference.value)

    def test_get_value_with_int(self):
        self.assertTrue(get_value(self.intPreference.name) == 10)

    def test_get_value_with_invalid_int(self):
        with self.assertRaises(ValueError):
            get_value(self.invalidIntPreference.name)

    def test_get_value_with_float(self):
        self.assertTrue(get_value(self.floatPreference.name) == 10.15)

    def test_get_value_with_invalid_float(self):
        with self.assertRaises(ValueError):
            get_value(self.invalidFloatPreference.name)

    def test_get_value_with_boolean(self):
        self.assertTrue(get_value(self.booleanTruePreference.name))

    def test_get_value_with_invalid_type(self):
        with self.assertRaises(ValueError):
            get_value(self.invalidTypePreference.name)
