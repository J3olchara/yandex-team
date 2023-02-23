# Generated by Django 3.2.15 on 2023-02-23 11:01

import core.validators
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20230222_1939'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'тэг', 'verbose_name_plural': 'тэги'},
        ),
        migrations.AlterField(
            model_name='category',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Да/Нет', verbose_name='опубликован'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Придумайте название', max_length=150, validators=[django.core.validators.MaxLengthValidator(150)], verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='normalized_name',
            field=models.CharField(editable=False, max_length=150, unique=True, verbose_name='нормализованное имя'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(help_text='Придумайте артикул(может состоять только из латинских букв, цифр, _ и -)', max_length=200, unique=True, validators=[core.validators.slug_validator, django.core.validators.MaxLengthValidator(200)], verbose_name='уникальный артикул'),
        ),
        migrations.AlterField(
            model_name='category',
            name='weight',
            field=models.PositiveSmallIntegerField(default=100, verbose_name='вес'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(help_text='Выберите категорию', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.category', verbose_name='категория'),
        ),
        migrations.AlterField(
            model_name='item',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Да/Нет', verbose_name='опубликован'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(help_text='Придумайте название', max_length=150, validators=[django.core.validators.MaxLengthValidator(150)], verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(to='catalog.Tag', verbose_name='тэги'),
        ),
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(help_text='Опишите объект', validators=[core.validators.ValidateMustContain('превосходно', 'роскошно')], verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Да/Нет', verbose_name='опубликован'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Придумайте название', max_length=150, validators=[django.core.validators.MaxLengthValidator(150)], verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='normalized_name',
            field=models.CharField(editable=False, max_length=150, unique=True, verbose_name='нормализованное имя'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(help_text='Придумайте артикул(может состоять только из латинских букв, цифр, _ и -)', max_length=200, unique=True, validators=[core.validators.slug_validator, django.core.validators.MaxLengthValidator(200)], verbose_name='уникальный артикул'),
        ),
    ]
