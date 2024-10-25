from django.core.management import call_command


def load_sample_product():
    fixtures = ['sample_product']
    load_fixtures(fixtures)


def load_sample_cart():
    load_sample_product()

    fixtures = ['sample_cart_with_items']
    load_fixtures(fixtures)


def load_sample_order():
    fixtures = ['sample_order']
    load_fixtures(fixtures)


def load_fixtures(fixtures):
    for fixture in fixtures:
        call_command('loaddata', fixture)
