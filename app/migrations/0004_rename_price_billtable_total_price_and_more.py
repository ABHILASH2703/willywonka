# Generated by Django 5.0.3 on 2024-06-01 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_caketable_chocolatetable_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billtable',
            old_name='price',
            new_name='total_price',
        ),
        migrations.RenameField(
            model_name='carttable',
            old_name='price',
            new_name='total_price',
        ),
        migrations.AddField(
            model_name='carttable',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='producttable',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]