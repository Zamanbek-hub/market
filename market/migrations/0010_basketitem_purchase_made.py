# Generated by Django 3.2.10 on 2021-12-19 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_auto_20211219_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketitem',
            name='purchase_made',
            field=models.BooleanField(default=False),
        ),
    ]
