# Generated by Django 5.1 on 2024-08-26 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_classification_product_available_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]
