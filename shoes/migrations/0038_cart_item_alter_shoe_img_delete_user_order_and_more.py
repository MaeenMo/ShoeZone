# Generated by Django 4.2 on 2023-04-15 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shoes", "0037_alter_shoe_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart_item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_qty", models.IntegerField()),
                ("selected_size", models.CharField(default="", max_length=80)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("ordered", models.BooleanField(default=False)),
                ("order_num", models.CharField(default="#000000", max_length=20)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="shoe",
            name="img",
            field=models.ImageField(upload_to="shoes_images"),
        ),
        migrations.DeleteModel(
            name="User_Order",
        ),
        migrations.AddField(
            model_name="cart_item",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shoes.shoe"
            ),
        ),
    ]