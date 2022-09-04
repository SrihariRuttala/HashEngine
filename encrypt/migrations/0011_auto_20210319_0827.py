# Generated by Django 2.2.12 on 2021-03-19 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encrypt', '0010_auto_20210308_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashes',
            name='sha224',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hashes',
            name='sha256',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hashes',
            name='sha384',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]