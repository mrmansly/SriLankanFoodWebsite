# Generated by Django 5.1 on 2024-09-03 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_contact_response_required_alter_contact_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'No Stars - Worst food ever!'), (1, '1 Star - I wish I had spent that money elsewhere'), (2, '2 Stars - Food was edible, but wont be coming back'), (3, '3 Stars - Was nice but nothing out of the ordinary'), (4, '4 Stars - Pretty, pretty, pretty good'), (5, '5 Stars - Oooh la la - Restaurant Quality')], default=None, null=True),
        ),
    ]
