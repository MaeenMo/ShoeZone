# Generated by Django 4.0.6 on 2023-04-02 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0032_shoe_shoe_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_order',
            name='order_num',
            field=models.CharField(default='#000000', max_length=20),
        ),
        migrations.AddField(
            model_name='user_order',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]
