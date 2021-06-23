# Generated by Django 3.2.4 on 2021-06-22 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mini_store_app', '0010_remove_cartitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mini_store_app.product'),
            preserve_default=False,
        ),
    ]