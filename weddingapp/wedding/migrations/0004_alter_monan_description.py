# Generated by Django 4.1.7 on 2023-03-29 17:23

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0003_monan_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monan',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
