# Generated by Django 3.2.15 on 2023-02-21 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_category_item_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.RemoveField(
            model_name='item',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
