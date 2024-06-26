# Generated by Django 5.0.3 on 2024-03-26 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0007_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="first name"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="last name"
            ),
        ),
    ]
