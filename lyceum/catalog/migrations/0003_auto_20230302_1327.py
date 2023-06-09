# Generated by Django 3.2.15 on 2023-03-02 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20230301_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='item_gallery',
        ),
        migrations.AddField(
            model_name='photogallery',
            name='item',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog.item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='main_image',
            field=models.ImageField(help_text='Выберите основное фото товара', upload_to='', verbose_name='основное фото'),
        ),
    ]
