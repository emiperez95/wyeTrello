# Generated by Django 3.2.9 on 2021-11-12 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='miniUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='user name')),
                ('trelloKey', models.CharField(max_length=50, verbose_name='trello key')),
                ('date', models.DateField(verbose_name='date added')),
            ],
            options={
                'verbose_name': 'miniUser',
                'verbose_name_plural': 'miniUsers',
            },
        ),
        migrations.CreateModel(
            name='album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='album_name')),
                ('artist', models.CharField(max_length=50, verbose_name='artist name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trellofy.miniuser', verbose_name='user')),
            ],
            options={
                'verbose_name': 'album',
                'verbose_name_plural': 'albums',
            },
        ),
    ]