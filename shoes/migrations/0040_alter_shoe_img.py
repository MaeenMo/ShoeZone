# Generated by Django 4.2 on 2023-05-07 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shoes", "0039_alter_shoe_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shoe",
            name="img",
            field=models.ImageField(upload_to="ShoeZone/static/Media"),
        ),
    ]
