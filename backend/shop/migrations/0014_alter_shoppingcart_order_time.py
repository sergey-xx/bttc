# Generated by Django 5.0.3 on 2024-03-27 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0013_alter_shoppingcart_order_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shoppingcart",
            name="order_time",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]