# Generated by Django 4.1.7 on 2023-03-20 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0019_shoe_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoe',
            name='sizes',
        ),
    ]
