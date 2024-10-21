# Generated by Django 5.1.1 on 2024-10-18 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_systempreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancelled_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='completed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='confirmation_sent_date',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]