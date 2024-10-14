from django.core.management import call_command


def load_sample_product():
    fixture = 'sample_product'
    call_command('loaddata', fixture)
