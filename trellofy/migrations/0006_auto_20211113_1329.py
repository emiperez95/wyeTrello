# Generated by Django 3.2.9 on 2021-11-13 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trellofy', '0005_auto_20211113_0806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='artist',
        ),
        migrations.AddField(
            model_name='album',
            name='year',
            field=models.CharField(default=None, max_length=5, verbose_name='album year'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=50, verbose_name='album name'),
        ),
        migrations.AlterField(
            model_name='miniuser',
            name='name',
            field=models.CharField(max_length=50, verbose_name='artist name'),
        ),
    ]
