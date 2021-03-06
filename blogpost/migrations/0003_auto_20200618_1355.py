# Generated by Django 3.0.7 on 2020-06-18 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0002_auto_20200618_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
