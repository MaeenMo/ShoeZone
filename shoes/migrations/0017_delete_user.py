# Generated by Django 4.1.7 on 2023-03-18 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0016_rename_name_user_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
