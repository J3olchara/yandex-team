# Generated by Django 3.2.15 on 2023-03-22 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='О пользователе'),
        ),
    ]