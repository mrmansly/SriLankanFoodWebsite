# Generated by Django 5.1 on 2024-09-03 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_contact_preferred_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='product',
        ),
        migrations.AddField(
            model_name='contact',
            name='products',
            field=models.ManyToManyField(related_name='contacts', to='main.product'),
        ),
    ]
