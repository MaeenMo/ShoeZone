# Generated by Django 4.2 on 2023-08-06 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shoes", "0042_alter_shoe_img"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart_item",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="cart_item",
            name="product",
        ),
        migrations.DeleteModel(
            name="Order",
        ),
        migrations.AlterField(
            model_name="shoe",
            name="img",
            field=models.ImageField(upload_to="shoes_images"),
        ),
        migrations.DeleteModel(
            name="Cart_item",
        ),
    ]
