# Generated by Django 3.2.9 on 2021-11-12 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trellofy', '0003_auto_20211112_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miniuser',
            name='date',
            field=models.DateTimeField(default=None, verbose_name='date added'),
        ),
    ]