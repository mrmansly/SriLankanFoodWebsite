# Generated by Django 5.1.1 on 2024-10-21 04:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_productstock_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productstock',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.product'),
        ),
    ]