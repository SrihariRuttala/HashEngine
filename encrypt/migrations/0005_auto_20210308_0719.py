# Generated by Django 2.2.12 on 2021-03-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encrypt', '0004_auto_20210307_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploads',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]
