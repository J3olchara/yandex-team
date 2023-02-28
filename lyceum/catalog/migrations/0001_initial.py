# Generated by Django 3.2.15 on 2023-02-28 20:03

import core.validators
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Да/Нет', verbose_name='опубликован')),
                ('name', models.CharField(help_text='Придумайте название', max_length=150, validators=[django.core.validators.MaxLengthValidator(150)], verbose_name='название')),
                ('slug', models.CharField(help_text='Придумайте артикул(может состоять только из латинских букв, цифр, _ и -)', max_length=200, unique=True, validators=[core.validators.slug_validator, django.core.validators.MaxLengthValidator(200)], verbose_name='уникальный артикул')),
                ('normalized_name', models.CharField(editable=False, max_length=150, unique=True, verbose_name='нормализованное имя')),
                ('weight', models.PositiveSmallIntegerField(default=100, verbose_name='вес')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='MainImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Загрузите фото', null=True, upload_to='uploads/main_images/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Главное изображение',
                'verbose_name_plural': 'Главные изображения',
            },
        ),
        migrations.CreateModel(
            name='PhotoGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Загрузите фото', null=True, upload_to='uploads/gallery/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Галерея',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Да/Нет', verbose_name='опубликован')),
                ('name', models.CharField(help_text='Придумайте название', max_length=150, validators=[django.core.validators.MaxLengthValidator(150)], verbose_name='название')),
                ('slug', models.CharField(help_text='Придумайте артикул(может состоять только из латинских букв, цифр, _ и -)', max_length=200, unique=True, validators=[core.validators.slug_validator, django.core.validators.MaxLengthValidator(200)], verbose_name='уникальный артикул')),
                ('normalized_name', models.CharField(editable=False, max_length=150, unique=True, verbose_name='нормализованное имя')),
            ],
            options={
                'verbose_name': 'тэг',
                'verbose_name_plural': 'тэги',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Да/Нет', verbose_name='опубликован')),
                ('name', models.CharField(help_text='Придумайте название', max_length=150, validators=[django.core.validators.MaxLengthValidator(150)], verbose_name='название')),
                ('text', models.TextField(help_text='Опишите объект', validators=[core.validators.ValidateMustContain('превосходно', 'роскошно')], verbose_name='описание')),
                ('category', models.ForeignKey(help_text='Выберите категорию', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.category', verbose_name='категория')),
                ('item_gallery', models.ManyToManyField(to='catalog.PhotoGallery', verbose_name='галерея')),
                ('main_image', models.ForeignKey(help_text='Выберите основное фото, для загрузки перейдите в таблицу Главные изображения', on_delete=django.db.models.deletion.CASCADE, to='catalog.mainimage', verbose_name='основное фото')),
                ('tags', models.ManyToManyField(to='catalog.Tag', verbose_name='тэги')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
    ]
