# Generated by Django 3.2.4 on 2021-06-22 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mini_store_app', '0007_auto_20210622_2153'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mini_store_app.product'),
            preserve_default=False,
        ),
    ]
