# Generated by Django 5.1.1 on 2024-11-09 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_cart_user_userdetails'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]