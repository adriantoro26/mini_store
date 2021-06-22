# Generated by Django 3.2.4 on 2021-06-21 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('lastLname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_seller', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('cart_id', models.ManyToManyField(to='mini_store_app.Cart')),
                ('creator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_store_app.user')),
                ('order_id', models.ManyToManyField(to='mini_store_app.Orders')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='buyer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_store_app.user'),
        ),
        migrations.AddField(
            model_name='cart',
            name='buyer_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mini_store_app.user'),
        ),
    ]