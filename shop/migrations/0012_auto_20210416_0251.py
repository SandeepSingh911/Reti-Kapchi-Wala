# Generated by Django 3.1.7 on 2021-04-15 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20210416_0144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderplaced',
            old_name='prodduct',
            new_name='product',
        ),
    ]
