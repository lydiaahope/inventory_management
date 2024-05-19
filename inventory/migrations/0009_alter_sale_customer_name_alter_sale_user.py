# Generated by Django 5.0.6 on 2024-05-19 16:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0008_sale_saleitem"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="sale",
            name="customer_name",
            field=models.CharField(default="Unknown Customer", max_length=100),
        ),
        migrations.AlterField(
            model_name="sale",
            name="user",
            field=models.ForeignKey(
                default="Unknown Customer",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
