# Generated by Django 5.1.1 on 2024-09-25 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_contact_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='contacts', to='main.product'),
        ),
    ]
