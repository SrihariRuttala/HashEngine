# Generated by Django 2.2.12 on 2021-03-08 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encrypt', '0007_auto_20210308_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploads',
            name='date_created',
        ),
    ]
