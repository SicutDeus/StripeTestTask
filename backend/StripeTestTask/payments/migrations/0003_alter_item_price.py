# Generated by Django 3.2.16 on 2022-11-18 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20221118_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(help_text='Введите стоимость предмета', verbose_name='стоимость предмета'),
        ),
    ]