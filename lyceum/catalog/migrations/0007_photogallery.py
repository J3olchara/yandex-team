# Generated by Django 3.2.15 on 2023-03-02 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_delete_photogallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Загрузите фото', upload_to='uploads/gallery/', verbose_name='фото')),
                ('item', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.item')),
            ],
            options={
                'verbose_name': 'Галерея',
                'verbose_name_plural': 'Галерея',
            },
        ),
    ]
