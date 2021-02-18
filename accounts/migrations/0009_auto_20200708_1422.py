# Generated by Django 3.0.8 on 2020-07-08 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0005_blogpost_content'),
        ('replies', '0002_auto_20200708_1422'),
        ('accounts', '0008_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='liked_posts',
            field=models.ManyToManyField(blank=True, to='blogpost.BlogPost'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='liked_replies',
            field=models.ManyToManyField(blank=True, to='replies.Reply'),
        ),
    ]
