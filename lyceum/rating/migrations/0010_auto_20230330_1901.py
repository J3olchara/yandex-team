# Generated by Django 3.2.15 on 2023-03-30 16:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_item_category'),
        ('users', '0005_auto_20230323_1916'),
        ('rating', '0009_rename_creation_date_evaluation_creation_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='change_datetime',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='creation_datetime',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='changed',
            field=models.DateTimeField(auto_now=True, help_text='Когда был изменён в последний раз', verbose_name='последнее изменение'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Когда был создан', verbose_name='Создан'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='item',
            field=models.ForeignKey(help_text='Товар, которому оставили отзыв', on_delete=django.db.models.deletion.CASCADE, related_name='item', to='catalog.item', verbose_name='товар'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(help_text='Пользователь оставивший отзыв', on_delete=django.db.models.deletion.CASCADE, related_name='user', to='users.userproxy', verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='value',
            field=models.PositiveSmallIntegerField(help_text='Значение оценки', validators=[django.core.validators.MaxValueValidator(5, message='Максимальное значение оценки - 5'), django.core.validators.MinValueValidator(1, message='Минимальное значение оценки - 1')], verbose_name='оценка'),
        ),
    ]
