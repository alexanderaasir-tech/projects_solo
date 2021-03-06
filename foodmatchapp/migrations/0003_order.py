# Generated by Django 2.2 on 2021-08-15 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodmatchapp', '0002_item_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_qty', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_ordered', to='foodmatchapp.Item')),
                ('user_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to='foodmatchapp.User')),
            ],
        ),
    ]
