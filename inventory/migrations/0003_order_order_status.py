# Generated by Django 5.0.6 on 2024-05-24 11:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "inventory",
            "0002_rename_inventory_item_cartitem_item_cart_created_at_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Processed", "Processed"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
    ]
