# Generated by Django 3.2.4 on 2021-06-24 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_store_app', '0013_auto_20210624_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
