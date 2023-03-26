# Generated by Django 3.2.15 on 2023-03-23 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='failed_attemps',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Неудачных попыток входа подряд'),
        ),
        migrations.AddField(
            model_name='profile',
            name='normalized_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Нормализованная почта'),
        ),
    ]