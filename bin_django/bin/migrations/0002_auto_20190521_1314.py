# Generated by Django 2.1.5 on 2019-05-21 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='current_ts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='last_ts',
            field=models.IntegerField(default=0),
        ),
    ]
