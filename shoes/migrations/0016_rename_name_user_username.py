# Generated by Django 4.1.7 on 2023-03-17 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0015_shoe_sizes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
    ]
