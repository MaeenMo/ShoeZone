# Generated by Django 4.1.7 on 2023-03-26 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0027_user_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='color_hexa',
            field=models.CharField(default='#000000', max_length=50),
        ),
    ]
