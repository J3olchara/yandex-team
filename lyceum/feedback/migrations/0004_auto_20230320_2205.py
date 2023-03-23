# Generated by Django 3.2.15 on 2023-03-20 19:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20230314_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='processing_status',
            field=models.CharField(choices=[('received', 'получено'), ('processing', 'в обработке'), ('answered', 'ответ дан')], default='received', max_length=100),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='feedback.sender', verbose_name='Отправитель'),
        ),
    ]
