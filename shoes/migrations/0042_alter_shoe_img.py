# Generated by Django 4.2 on 2023-07-27 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shoes", "0041_alter_shoe_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shoe",
            name="img",
            field=models.ImageField(upload_to="ShoeZone/static/Media"),
        ),
    ]