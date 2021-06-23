# Generated by Django 3.2.4 on 2021-06-22 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_store_app', '0005_auto_20210622_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
