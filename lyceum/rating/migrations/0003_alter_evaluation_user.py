# Generated by Django 3.2.15 on 2023-03-27 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230323_1916'),
        ('rating', '0002_alter_evaluation_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userproxy'),
        ),
    ]
