# Generated by Django 3.2.15 on 2023-03-27 05:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='value',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5, message='Максимальное значение оценки - 5'), django.core.validators.MinValueValidator(1, message='Минимальное значение оценки - 1')], verbose_name='оценка'),
        ),
    ]
