# Generated by Django 3.2.15 on 2023-03-29 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0004_evaluation_change_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluation',
            old_name='Change_time',
            new_name='change_datetime',
        ),
    ]