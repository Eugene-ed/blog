# Generated by Django 4.0.5 on 2022-06-23 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(default=3, verbose_name='Rating'),
        ),
    ]
