# Generated by Django 5.0.3 on 2024-03-28 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0021_alter_item_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="shoppingcart",
            name="payment_id",
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
