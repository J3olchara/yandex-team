# Generated by Django 3.2.15 on 2023-03-29 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0003_alter_evaluation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='Change_time',
            field=models.DateTimeField(auto_now=True, verbose_name='дата и время изменения или создания'),
        ),
    ]
