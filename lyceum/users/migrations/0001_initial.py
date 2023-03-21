# Generated by Django 3.2.15 on 2023-03-20 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(verbose_name='birth date')),
                ('image', models.ImageField(default='uploads/cat.jpg', upload_to='', verbose_name='avatar')),
                ('coffee_count', models.IntegerField(default=0, verbose_name='coffee attemps count')),
            ],
            options={
                'verbose_name': 'Дополнительное поле',
                'verbose_name_plural': 'Дополнительные поля',
            },
        ),
    ]
