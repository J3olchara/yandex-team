# Generated by Django 3.2.15 on 2023-03-06 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20230303_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_on_main',
            field=models.BooleanField(default=False, help_text='показывать товар на главной странице?', verbose_name='показать на главной'),
        ),
    ]
