# Generated by Django 5.1.1 on 2024-09-25 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_faq_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, related_name='contacts', to='main.product'),
        ),
    ]
